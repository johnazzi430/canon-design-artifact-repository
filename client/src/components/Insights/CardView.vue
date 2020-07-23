

<template lang="html">
  <div class="container" style="margin-top:0px">
    <div class="md-form mt-0" id="card-search">
      <input v-model="search"
        class="form-control"
        type="text"
        placeholder="Search for user insight"
        aria-label="Search">
    </div>

    <br>

    <b-card-group columns>
      <b-card class="card" v-for="card in filterItems(cards)"
              v-bind:key="card.name"
              v-bind:class="card.experience_vector"
              v-on:click = 'OpenDetail(card.id)'>
        <b-card-text>
          <span>{{card.title}}</span>
          <!-- <span class="badge badge-pill badge-success"
            v-bind:class="card.experience_vector">
            {{card.experience_vector}}</span> -->
          <!-- <span><b-button href="javascript:void(0)" v-on:click = 'OpenDetail(card.id)'
              variant="outline-secondary">Open insight</b-button>
          </span> -->
        </b-card-text>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import api from '../../api'
import {EventBus} from "../../index.js";



export default {
  data() {return {
    cards : [],
    search : '',
    columns: 4
  }
 },
  async mounted() {
    const {data} = await api.insightTable()
    this.cards = data

    let self = this
    EventBus.$on('insight-data-changed', async function(){
      const {data} = await api.insightTable()
      self.cards = data
    })
  },
  methods:{
    OpenDetail(id) {
      EventBus.$emit('insight-selection-changed' ,this.selectedRow = id)
    },

    filterItems: function(cards) {
      var self = this;
      return cards.filter(function(cards) {
        let regex = new RegExp('(' + self.search+ ')', 'i');
//        return cards.name.match(regex);
        return JSON.stringify(cards).match(regex);
      })
    }
  },
};

</script>

<style lang="scss" scoped>

.card-columns {
    column-count: 4;
}

@media only screen and (max-width: 400px) {
  .card-columns {
      column-count: 1;
  }
}

.card{
  border-left-style: solid;
  border-left-width: thick;
  box-shadow:
    -8px -8px 8px 0 rgba(255,255,255,0.4),
    8px 8px 8px 0 rgba(0,0,0,0.05);

  &:hover{
    background: #E5E5E5;
  }

  &:active {
    background: #D9D9D9;
  }

  &span{
    width:100%;
    display: block;
  }
}

.card-text{
  font-size: inherit;
}

.avatar {
  min-width: 50px;
  max-width: 50px;
  min-height: 50px;
  max-height: 50px;
  display: block;
  margin-left: auto;
  margin-right: auto;
  border-radius: 50%;
}

.badge.Negative{
  background-color: #FF5C42
}

.badge.Positive{
  background-color: green
}

.badge.Neutral{
  background-color: grey
}

.card.Negative{
  border-left-color: #FF5C42
}

.card.Positive{
  border-left-color: green
}

.card.Neutral{
  border-left-color: grey
}


</style>
