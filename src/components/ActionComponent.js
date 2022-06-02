import React from "react";

function Action(props) {

    const renderType = () => {

        if(props.editing === true)  {
            return(<input type="text" className="action editing" value={props.obj.value}/>);
        } 

        return(<p className="action">{props.obj.value}</p>);
    }

    return( 
        renderType()
    )
}

export default Action;