const fetch = require('node-fetch');

let baseUrl = "http://localhost:9899/"

export function getData(url){
  return fetch(baseUrl+url)
  .then(response => response.json())
  .then(data =>{return data})
  .catch(error => console.error(error));
}

export function setData(url, data) {
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