import { Component } from "react";


class Page extends Component {


    render() {

        const data = [
            {
                "type": "clip",
                "value": "CLIP NUMBER m15 s05 t05 050"
            }, 
            {
                "type": "scene",
                "value": "INT. MEDICAL ASSESSMENT UNIT - DAY - SD2"
            }, 
            {
                "type": "action",
                "value": "Following on from Clip 5. Steve in the bed, Elaine sitting beside it, the Nurse arives as the bedside."
            }, 
            {
                "type": "dialogue",
                "character": "Nurse",
                "parenthetical": "Friendly and energised", 
                "value": "Hello. How's the patient?"
            }, 
            {
                "type": "dialogue",
                "character": "Elaine",
                "value": "He keeps saying 'Please' over and over."
            }, 
            {
                "type": "dialogue",
                "character": "Nurse",
                "value": "What is it you want, Steve?"
            }, 
            {
                "type": "action",
                "value": "The nurse points at the glass of water, Steve shakes his head. Steve points at the bed."
            },
            {
                "type": "dialogue",
                "character":"Nurse",
                "value": "Here?"
            }, 
            {
                "type": "action",
                "value": "Steve nods."
            }
        ]


        return(
            <div className="page letter">
                <div className="page-content">
                    {
                        data.map((e) => {
                            switch(e.type) {
                                case "clip":
                                    return (<p className="clip">{e.value}</p>);

                                case "scene":
                                    return (<p className="scene">{e.value}</p>);

                                case "action":
                                    return (<p className="action">{e.value}</p>);

                                case "dialogue":
                                    return (
                                        <>
                                            <p className="character">{e.character}</p>
                                            {
                                                e.parenthetical !== null ?
                                                    <></> : 
                                                <p className="parenthetical">{e.parenthetical}</p>
                                            }
                                            <p className="dialogue">{e.value}</p>
                                        </>
                                    );
                                    break;
                            }
                        })

                    }
                </div>
            </div>
        );
    }



}

export default Page;