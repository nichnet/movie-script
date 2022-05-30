import { Component } from "react";
import Clip from "./ClipComponent";
import Scene from "./SceneComponent";
import Action from "./ActionComponent";
import Dialogue from "./DialogueComponent";
import Transition from "./TransitionComponent";
import Header from "./HeaderComponent";


class Page extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        var sceneIndex = 0;

        return(
            <div className="page letter">
                <div className="page-content">
                    <Header page={this.props.data.page}/>

                    {
                        this.props.data.content.map((e) => {
                            switch(e.type) {
                                case "clip":
                                    return ( <Clip value={e.value}/> );

                                case "scene":
                                    sceneIndex++;
                                    return ( <Scene index={sceneIndex} value={e.value}/> );

                                case "transition":
                                    return ( <Transition value={e.value}/> );

                                case "action":
                                    return ( <Action value={e.value}/> );

                                case "dialogue":
                                    return ( <Dialogue value={e}/> );
                            }
                        })
                    }
                </div>
            </div>
        );
    }



}

export default Page;