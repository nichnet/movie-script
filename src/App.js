import React from 'react';
import './style.css';
import Pages from './components/PagesComponent';
import example_data from './example_data';
import { Col, Container, Row } from 'react-bootstrap';


//

function App() {
    return( 
        <div className="container-fluid d-flex">
                <Col xs={9} xl={10} className="workarea">
                    <Pages pages={example_data}/>
                </Col>

                <Col xs={3} xl={2} className="test3">

                </Col>
        </div>


         
    )
}

export default App;