const fetch = require('node-fetch');

let baseUrl = "http://localhost:9899/"

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

  export function setPlayConfig(data){
    return fetch(baseUrl + "setPlayConfig", {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data), 
    })
    .then(response => response.json())
    .then(data =>{return data})
    .catch(error => console.error(error));
  }