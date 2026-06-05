import {request} from "./requestConfig";


export function getMainMenu(){
    return request({
        url:"/main_menu",
    })
}