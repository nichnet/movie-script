import React from 'react';
import './style.css';
import Pages from './components/PagesComponent';
import example_data from './example_data';
import { Col, Container, Row } from 'react-bootstrap';
import Tabs from 'react-bootstrap/Tabs';
import Tab from 'react-bootstrap/Tab';

//

function App() {
    return( 
        <div className="d-flex">
                <Col xs={8} xl={10}>
                    <Row className="test5 workarea">
                        <Pages pages={example_data}/>
                    </Row>
                    <Row className="test4">
                    </Row>
                </Col>

                <Col xs={4} xl={2} className="test3">
                    <Tabs>
                        <Tab eventKey="first" title="Scenes">
                            <p>blah 1</p>
                        </Tab>

                        <Tab eventKey="fourth" title="Characters">
                            <p>blah 1</p>
                        </Tab>

                        <Tab eventKey="third" title="Document">
                            <p>blah 1</p>
                        </Tab>
                    </Tabs>
                </Col>
        </div>


         
    )
}

export default App;