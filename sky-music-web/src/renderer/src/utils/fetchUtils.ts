let baseUrl = "http://127.0.0.1:9899/"

export function getList(listName,searchStr){
  return fetch(baseUrl+"?listName="+listName+"&searchStr="+searchStr)
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
    return fetch(baseUrl + "config_operate", {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "name":name,
        "value":value,
        "operate":'set'
      }), 
    })
    .then(response => response.json())
    .then(data =>{return data})
    .catch(error => console.error(error));
  }

  export function getWWWData(url){
    return fetch(url)
    .then(response => response.text())
    .then(data =>{return data})
    .catch(error => console.error(error));
  }