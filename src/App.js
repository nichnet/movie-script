import logo from './logo.svg';
import { Col, Container, Row } from 'react-bootstrap';
import './App.css';
import Page from './components/PageComponent';

function App() {
  return (
    <div className="App">
      <Container>
        <Col>
        
          <Row/>
          <Page/>
          <Page/>
        </Col>
      </Container>
    </div>
  );
}

export default App;
