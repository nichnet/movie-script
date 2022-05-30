import { Component } from "react";
import { Col, Container, Row } from 'react-bootstrap';
import './App.css';
import Page from './components/PageComponent';

class App extends Component {

  render() {
    const data = [
      {
        "page": 1,
        "content": [
          {
            "type":"transition",
            "value": "Fade In"
          },
          {
            "type": "clip",
            "value": "CLIP NUMBER m15 s05 t05 050"
          }, 
          {
            "type": "scene",
            "value": "INT. MEDICAL ASSESSMENT UNIT - DAY - SD2"
          }, 
          {
            "type": "action",
            "value": "Following on from Clip 5. Steve in the bed, Elaine sitting beside it, the Nurse arives as the bedside."
          }, 
          {
            "type": "dialogue",
            "character": "Captain Kurk",
            "voiceover": true,
            "offscreen": false,
            "parenthetical": "Friendly and energised", 
            "value": "Captain's log, Stardate 1513.1. Our position, orbiting planet M-113. On board the Enterprise, Mister Spock temporarily in command. On the planet the ruins of an ancient and long-dead civilisation. Ship's surgeon McCoy and myself are now beaming down to the planet's surface. Our mission, routine medical examination of archaeologist Robert Crater and his wife Nancy. Routine but for the fact that Nancy Crater is that one woman in Doctor McCoy's past."
          }, 
          {
            "type": "dialogue",
            "character": "Elaine",
            "offscreen": true,
            "value": "He keeps saying 'Please' over and over."
          }, 
          {
            "type": "dialogue",
            "character": "Nurse",
            "value": "What is it you want, Steve?"
          }, 
          {
            "type": "action",
            "value": "The nurse points at the glass of water, Steve shakes his head. Steve points at the bed."
          },
          {
            "type": "dialogue",
            "character":"Nurse",
            "value": "Here?"
          }, 
          {
            "type": "action",
            "value": "Steve nods."
          }
        ]
      },
      {
        "page": 2,
        "content": [
          {
            "type": "scene",
            "value": "CLIP NUMBER m15 s05 t05 050"
          }, 
        ]
      }
    ];

    return (
      <div className="App">
        <Container>
          <Col> 
          {
            data.map((e) => {
              return(
                <>
                  <Row/>
                  <Page data={e}/>
                </>
              )
            })
          }
          </Col>
        </Container>
      </div>
    );
  }
}
export default App;
