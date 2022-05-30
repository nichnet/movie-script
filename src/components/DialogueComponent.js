import { Component } from "react";

class Dialogue extends Component {

    constructor(props) {
        super(props);
    }

    render() {

        var characterLabel = this.props.value.character;

        if(this.props.value.voiceover == true ||
            this.props.value.offscreen == true) {
            
            characterLabel += " (";
            
            if(this.props.value.voiceover == true) {
                characterLabel += "v.o.";
            }

            if(this.props.value.voiceover == true && 
                this.props.value.offscreen == true) {
               characterLabel += ", ";
            }

            if(this.props.value.offscreen == true) {
                characterLabel += "o.s.";
            }

            characterLabel += ")";
        }

        return(
            <>
                <p className="character">{characterLabel}</p>

                {
                    this.props.value.parenthetical !== undefined ? 
                    <p className="parenthetical">({this.props.value.parenthetical})</p>
                    :
                    <></>
                }

                <p className="dialogue">{this.props.value.value}</p>
            </>

        );
    }
}

export default Dialogue;