import { Component } from "react";

class Scene extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return(
            <div>
                <p className="scene">{this.props.value}</p>
                <p>{this.props.index}</p>
            </div>

        );
    }
}

export default Scene;