import { Component } from "react";

class Action extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return(

            <p className="action">{this.props.value}</p>

        );
    }
}

export default Action;