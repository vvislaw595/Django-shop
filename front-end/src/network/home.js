import {request} from "./requestConfig.js"


export function getMainMenu(){
	return request({
		url:"/main_menu/",
	})
}

export function getSecondMenu(mainMenuId){
	return request({
		url:"/sub_menu/?main_menu_id="+mainMenuId,
	})
}

export function getFindGoods(mainMenuId){
	return request({
		url:"goods/find/"
	})
}

export function getCategoryGoods(categoryId, page){
	return request({
		url:"/goods/category/"+categoryId+"/"+page,
	})
}