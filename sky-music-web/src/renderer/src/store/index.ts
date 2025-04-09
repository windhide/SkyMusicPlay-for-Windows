import { createStore } from 'vuex'

export default createStore({
  state: {
    playList:[],
  },
  getters: {
    getPlayList(state) {
      return state.playList;
    },
    getNextPlayMusic(state){
      const needReturn = state.playList[0]
      state.playList.splice(0, 1)
      return needReturn
    }
  },
  mutations: {
    setPlayList(state, datas) {
      state.playList = datas;
    },
    addPlayList(state:any, data) {
      let addFlag = true
      state.playList.forEach(element => {
        if(element.truthName === data.truthName){
          addFlag = false;
          return;
        }
      });
      if(addFlag)
      state.playList.push({'name': data.name ,'truthName':data.truthName, 'type': data.type})
    },
    removePlayList(state:any, index:number){
      console.log("删除下标",index)
      state.playList.splice(index, 1)
    },
    clearPlayList(state:any){
      state.playList = []
    }
  },
  actions: {
  },
  modules: {}
})
