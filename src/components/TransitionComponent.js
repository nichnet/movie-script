import { Component } from "react";

class Transition extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return(

            <p className="transition">{this.props.value}:</p>

        );
    }
}

export default Transition;