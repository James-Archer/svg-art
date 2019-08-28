import React from 'react';
import './App.css';
import logo from './logo.svg'
import request from 'request';
import Slider from '@material-ui/core/Slider';
import { SliderPicker } from 'react-color';
import { saveAs } from 'file-saver';

//const MY_IP = "jamesarcher.pythonanywhere.com/"
const MY_IP = "http://localhost:5000/"


class App extends React.Component {

  constructor(props)
  {
    super(props);
    this.state = 
    {
      receivedText: "<None>",
      svgData: null,
      artists: ["None"],
      selectedArtist: null,
      artistInputs: null,
      artistToSend: {},
      waiting: false
    };
    this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
    this.handleArtistListChange = this.handleArtistListChange.bind(this);
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

    var toSend = this.state.artistToSend;

    if (!this.state.waiting){
      this.setState({waiting: true})
      request.post(MY_IP + "sendprops",
        {form:{
          width: this.state.width/2,
          height: this.state.height,
          args: toSend}}, (error, response, body)=>
      {
        console.error('error:', error); // Print the error if one occurred
        console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
        console.log('body:', body); // Print the HTML for the Google homepage.
        this.setState({
          svgData: body,
          waiting: false
        });
        
      });
  }
  }

  getArtists(){
    request.get(MY_IP + "artists",
      (error, response, body)=>
    {
      //console.error('error:', error); // Print the error if one occurred
      //console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
      //console.log('body:', body); // Print the HTML for the Google homepage.
      this.setState({
        artists: JSON.parse(body),
      });
      this.setState({selectedArtist: this.state.artists[0]});
      this.getArtistInputs(this.state.artists[0]);
    });
  }

  getArtistInputs(artist){
    request.post(MY_IP + 'artist_inputs',
      {form:{
        artist: artist
      }}, (error, response, body)=>
    {
      console.error('error:', error); // Print the error if one occurred
      console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
      console.log('body:', body); // Print the HTML for the Google homepage.
      this.setState({artistInputs: JSON.parse(body)})

      const ATS = {};
      Object.entries(this.state.artistInputs).map(
        ([input, params]) =>
        {
            ATS[params["name"]] = params["default"]
        })
      this.setState({artistToSend: ATS})
      //this.renderArtist()
    });
  }

  renderArtist(){
    console.log(this.state.artistToSend)
    if (this.state.artistInputs == null){
      console.log("No artist loaded")
      return
    }
    var toRender = []
    console.log("Artist is loaded")
    Object.entries(this.state.artistInputs).map(
      ([input, params]) =>
      {
          console.log(input, params["type"])
          const tp = params["type"]
          if (tp === "int")
          {toRender.push(
          <div>
            <text>{params["name"]}</text>
            <Slider min={params["min"]}
                    max={params["max"]}
                    defaultValue={params["default"]}
                    onChangeCommitted={(event, value) => {
                      const ATS = this.state.artistToSend
                      ATS[params["name"]] = value
                      this.setState({artistToSend: ATS}, () => this.sendProps());
                    }}
              />
              </div>
          )}
          if (tp === "color")
          {
            toRender.push(
            <div>
              <SliderPicker className="color-slider"
                      color={ this.state.artistToSend[params["name"]] }
                      onChangeComplete={(color) => {
                        const ATS = this.state.artistToSend
                        ATS[params["name"]] = color.hex
                        this.setState({artistToSend: ATS}, () => this.sendProps());
                      }}
              />
                </div>
            )}
      })
      return toRender
  }

  handleColorChange = (color) => {
    this.setState({color: color.hex });
    this.sendProps();
  }

  handleArtistListChange (event) {
    console.log(event.target.value)
    this.setState({selectedArtist: event.target.value})
    this.getArtistInputs(event.target.value)
  }

  saveImage()
  {
    if (this.state.svgData === null){return}
    var blob = new Blob([this.state.svgData], {type: "text/plain;charset=utf-8"});
    saveAs(blob, "my-image.svg");
  }

  render(){

    var artSelect
    var svgColumn

    if (this.state.artists[0] === "None")
    {
      this.getArtists();
      artSelect = <p>Waiting...</p>
    }
    else
    {
      artSelect =
      <form onSubmit={this.handleArtistListChange}>
      <label>
        <div>Pick artist:</div>
        <select  className="App-dropdown" value={this.state.selectedArtist} onChange={this.handleArtistListChange}>
          {this.state.artists.map((option) =>
          {
            return (<option className="App-dropdown" value={option}>{option} </option>)
          }
            )}
        </select>
      </label>
    </form>
    }

    if(this.state.svgData === null)
    {
      svgColumn = <img className="App-logo" src={logo} />
    }
    
    else
    {
      svgColumn = <div dangerouslySetInnerHTML={{ __html: this.state.svgData}}/>
    }
    return (
        <div className="row">
          <div className="column">
            {artSelect}
            
            {this.renderArtist()}

            <button className='button'
                disabled={this.state.waiting}
                onClick={()=>this.sendProps()}>
              Redraw!
            </button>

            <button className='button'
                onClick={()=>this.saveImage()}>
              Save image!
            </button>

          </div>
          <div className="columnSVG">
            {svgColumn}
          </div>
        </div>
    );
}
}

export default App;
