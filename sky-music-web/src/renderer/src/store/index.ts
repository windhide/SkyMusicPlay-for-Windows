import { createStore } from 'vuex'

export default createStore({
  state: {
    playList:[]
  },
  getters: {
    getPlayList(state) {
      return state.playList;
    }
  },
  mutations: {
    setPlayList(state, datas) {
      state.playList = datas;
    },
    addPlayList(state:any, name:any) {
      state.playList.push({'name': name})
    },
    removePlayList(state:any, index:number){
      console.log("删除下标",index)
      state.playList.splice(index, 1)
    }
  },
  actions: {
    updatePlayList({ commit }, newDatas) {
      commit('setPlayList', newDatas);
    }
  },
  modules: {}
})
