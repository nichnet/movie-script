import React from "react";

function Scene({obj}) {

    const interiorOrExterior = () => {
        if(obj.show_int_ext === true) {
            if(obj.int === true) {
                return "INT. ";
            } else {
                return "EXT. ";
            }
        }
    }

    return( 
        <p className="scene">{interiorOrExterior()}{obj.value}</p>
    )
}

export default Scene;