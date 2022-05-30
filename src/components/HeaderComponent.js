import { Component } from "react";

class Header extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return(
            <div className="header">
                <p className="pagenumber">{this.props.page}</p>
            </div>

        );
    }
}

export default Header;