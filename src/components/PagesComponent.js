import React, {useState, useRef} from 'react';
import Header from './HeaderComponent';
import Action from './ActionComponent';
import Scene from './SceneComponent';
import Clip from './ClipComponent';
import Dialogue from './DialogueComponent';
import Transition from './TransitionComponent';
import { Row } from 'react-bootstrap';

function Pages({pages}) {

    const [list, setList] = useState(pages);
    const [dragging, setDragging] = useState(false); //not dragging by default

    const dragElement = useRef();
    const dragNode = useRef();

    const handleDragStart = (e, params) => {
        console.log("drag start: " + params.toString());
        dragElement.current = params;
        
        dragNode.current  = e.target;
        dragNode.current.addEventListener('dragend', handleDragEnd);

//        setTimeout(() => {
            setDragging(true);//set dragging state in an asynchronous manner to fix stylgin.
  //      }, 0);

    }

    const handleDragEnter = (e, params) => {
        console.log("dragging");
        
        const currentElement = dragElement.current;

        //fires when user is dragging and moving over other elements
        if(e.target !== dragNode.current) {
            console.log("target is another element");

            setList(oldList => {
                //make new list to manipulate , this will set pages list.
                let newList = JSON.parse(JSON.stringify(oldList));//deep copy, but not very effecient (still better than a shallow copy).
                //the page the element is located at
                newList[params.pageIndex].content.splice(
                    //flip the two elements that were swapped
                    params.elementIndex, 
                    0, 
                    newList[currentElement.pageIndex].content.splice(
                        currentElement.elementIndex, 1
                    )[0]//return 0th item as the item to swap
                );

                //current item is now target item
                dragElement.current = params;

                console.log(JSON.stringify(newList));
                return newList;
            })
        }
    }

    const handleDragEnd = () => {
        console.log("drag end");
        dragElement.current = null;

        dragNode.current.removeEventListener('dragend', handleDragEnd);
        dragNode.current = null;
      
        setDragging(false);//set dragging state.
    }

    const getDraggingStyles = (params) => {
        //pass in page index  and element index to get unique element
        const currentElement = dragElement.current;

        if(currentElement.pageIndex === params.pageIndex && 
            currentElement.elementIndex === params.elementIndex) {
            return 'current-drag dnd-item';//if dragging, then return dnd-item AND current-drag
        }

        return 'dnd-item';
    }


    const renderSwitch = (param) => {
        switch(param.type) {
            case "clip":
                return (<Clip  obj={param}/>);

            case "scene":
                return ( <Scene obj={param}/> );

            case "transition":
                return ( <Transition obj={param}/> );

            case "action":
                return ( <Action obj={param}/> );

            case "dialogue":
                return ( <Dialogue obj={param}/> );
        }
      }

    return(
        <Row className="">
            {
                list.map((page, pageIndex) => (
                    <div key={page.page_number} className="page letter">
                        <Header value={page.page_number}/>
                        <div 
                        
                        onDragEnter = {
                            dragging && !page.content.length ? 
                            (e) => handleDragEnter(e, {pageIndex, elementIndex:  0}) 
                            :
                            null
                        }

                        key={page.page_number} 
                        className="page-content"
                        >
                            {
                                page.content.map((element, elementIndex) =>(
                                    <div 
                                        draggable 
                                        onDragStart = {
                                            (e) => { 
                                                handleDragStart(e, {pageIndex, elementIndex})
                                            }
                                        } 
                                        onDragEnter = {
                                            dragging ? 
                                            (e) => handleDragEnter(e, {pageIndex, elementIndex})
                                            : 
                                            null
                                        }
                                        
                                        key={page.page_number + ":" + elementIndex} 
                                        className={dragging ? getDraggingStyles({pageIndex, elementIndex}) : "dnd-item"}>
                                            {
                                                renderSwitch(element)
                                            }
                                        </div>
                                ))
                            }
                        </div> 
                    </div>
                ))
            }
        </Row>
    )
}

export default Pages;