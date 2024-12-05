const fetch = require('node-fetch');

let baseUrl = "http://127.0.0.1:9899/"

export function getList(listName){
  return fetch(baseUrl+"?listName="+listName)
  .then(response => response.json())
  .then(data =>{return data})
  .catch(error => console.error(error));
}

export function getData(url){
  return fetch(baseUrl+url)
  .then(response => response.json())
  .then(data =>{return data})
  .catch(error => console.error(error));
}

export function sendData(url, data) {
  console.log("data",data)
  return fetch(baseUrl + url, {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data), 
  })
  .then(response => response.json())
  .then(data =>{return data})
  .catch(error => console.error(error));}

  export function setConfig(name,value){
    return fetch(baseUrl + "setConfig", {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "name":name,
        "value":value
      }), 
    })
    .then(response => response.json())
    .then(data =>{return data})
    .catch(error => console.error(error));
  }