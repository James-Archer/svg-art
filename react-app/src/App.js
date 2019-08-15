import React from 'react';
import './App.css';
import request from 'request';
import Slider from '@material-ui/core/Slider';
import { SliderPicker } from 'react-color';

class App extends React.Component {

  constructor(props)
  {
    super(props);
    this.state = 
    {
      receivedText: "<None>",
      svgData: null,
      n: 30,
      color: 'black',
      thickness: 2
    };
    this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
  }

  componentDidMount() {
    this.updateWindowDimensions();
    window.addEventListener('resize', this.updateWindowDimensions);
  }
  
  componentWillUnmount() {
    window.removeEventListener('resize', this.updateWindowDimensions);
  }

  updateWindowDimensions() {
    this.setState({ width: window.innerWidth, height: window.innerHeight });
  }

  sendProps(){
    request.post('http://localhost:5000/sendprops',
      {form:{
        width: this.state.width,
        height: this.state.height,
        n: this.state.n,
        color: this.state.color,
        thickness: this.state.thickness
      }}, (error, response, body)=>
    {
      console.error('error:', error); // Print the error if one occurred
      console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
      console.log('body:', body); // Print the HTML for the Google homepage.
      this.setState({
        svgData: body,
      });
    });
  }

  handleColorChange = (color) => {
    this.setState({color: color.hex });
    this.sendProps();
  }

  render(){
    return (
        <div className="row">
          <div className="column">
            <p>Diagonal Lines</p>
            <SliderPicker
                    color={ this.state.color }
                    onChangeComplete={(color) => {
                      this.setState({color: color.hex });
                      this.sendProps();
                    }}
            />
            <text>Resolution</text>
            <Slider aria-label='Resolution'
                    min={10}
                    max={100}
                    defaultValue={30}
                    onChangeCommitted={(event, value) => {
                      this.setState({ n: value });
                      this.sendProps();
                    }}
              />

            <text>Thickness</text>
            <Slider aria-label='Thickness'
                    min={1}
                    max={10}
                    defaultValue={2}
                    onChangeCommitted={(event, value) => {
                      this.setState({ thickness: value });
                      this.sendProps();
                    }}
              />

            <button className='button'
                onClick={()=>this.sendProps()}>
              Redraw!
            </button>

          </div>
          <div className="columnSVG">
            <div dangerouslySetInnerHTML={{ __html: this.state.svgData}}/>
          </div>
        </div>
    );
}
}

export default App;
