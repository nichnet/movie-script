import { Component } from "react";

class Header extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return(
            <div className="page-header">
                <p className="page-number">{this.props.value}.</p>
            </div>
        )
    }
}

export default Header;