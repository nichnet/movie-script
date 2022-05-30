import { Component } from "react";

class Clip extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return(

            <p className="clip">{this.props.value}</p>

        );
    }
}

export default Clip;