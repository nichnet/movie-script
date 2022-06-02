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

    const create = (parenthetical, value) => {
        return (
            <>
                {
                    parenthetical !== undefined ? 
                    <p className="parenthetical">({parenthetical})</p>
                    :
                    null
                }
                <p className="dialogue">{value}</p>
            </>
        );
    }
/*


*/

    const createDialogue = () => {

        if(typeof obj.value === "string") {
            return create(obj.parenthetical !== undefined ? obj.parenthetical : undefined, obj.value);
        } else {
            //array
            return (
                obj.value.map((o) => {
                    return create(o.parenthetical !== undefined ? o.parenthetical : undefined, o.value)
                })
            );
        }
    }

    return ( 
        <>
            <p className="character">{characterLabel()}</p>
            {
                createDialogue()
            }
        </>
    )
}

export default Dialogue;