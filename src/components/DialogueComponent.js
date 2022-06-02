import React from "react";

function Dialogue({obj}) {

    const characterLabel = () => {

        var characterLabel = obj.character;

        if(obj.voiceover == true ||
            obj.offscreen == true) {
            
            characterLabel += " (";
            
            if(obj.voiceover == true) {
                characterLabel += "v.o.";
            }

            if(obj.voiceover == true && 
                obj.offscreen == true) {
               characterLabel += ", ";
            }

            if(obj.offscreen == true) {
                characterLabel += "o.s.";
            }

            characterLabel += ")";
        }

        return characterLabel;
    }

    return( 
        <>
            <p className="character">{characterLabel()}</p>

            {
                obj.parenthetical !== undefined ? 
                <p className="parenthetical">({obj.parenthetical})</p>
                :
                <></>
            }

            <p className="dialogue">{obj.value}</p>
        </>
    )
}

export default Dialogue;