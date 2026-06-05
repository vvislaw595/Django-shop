import {request} from "@/network/requestConfig.js";

export function addAddressData(data) {
    return request({
        url:"/address/",
        method:"post",
        data
    })
}

export function getAllAddressesData() {
    return request({
        url:"/address/",
        method:"get",
    })
}

export function editAllAddressData(data) {
    return request({
        url:"/address/edit",
        method:"post",
        data
    })
}

export function deleteAddressData(data) {
    return request({
        url:"/address/delete",
        method:"post",
        data
    })
}