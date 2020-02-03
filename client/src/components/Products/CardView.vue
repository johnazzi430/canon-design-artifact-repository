

<template lang="html">
  <div class="container">
    <div class="row">
      <div class="md-form mt-0 col-8" id="card-search">
        <input v-model="search"
          class="form-control"
          type="text"
          placeholder="Search for product"
          aria-label="Search">
      </div>
      <h4>Filter: </h4>
          <b-button-group class="mx-1">
            <b-button variant="info"
            @click='toggleSearch("collins")'>Collins</b-button>
            <b-button variant="info"
            @click='toggleSearch("pratt")'>Pratt</b-button>
          </b-button-group>
          <b-button-group class="mx-1">
            <b-button variant="info"
            @click='toggleSearch(`"external":0`)'>Internal</b-button>
            <b-button variant="info"
            @click='toggleSearch(`"external":1`)'>External</b-button>
          </b-button-group>
    </div>
    <br>

    <b-card-group columns>
      <b-card class="card" v-for="card in filterItems(cards)" v-bind:key="card.name">
        <b-card-text>
          <h5 style="text-align:center">{{card.name}}</h5>
          <p class="well">
            {{card.description}}
          </p>
          <b-button v-b-toggle="'collapse-'+card.id"
            variant="outline-secondary">More Detail</b-button>
               <!-- class="stretched-link " -->
          <b-button href="javascript:void(0)" v-on:click = 'OpenDetail(card.id)'
              variant="outline-secondary">Open Product</b-button>
          <b-collapse :id="'collapse-'+card.id" class="mt-2">
              <label>Product Goals</label>
              <p class="text-wrap"> {{card.goals}} </p>
              <label>Features</label>
              <p> {{card.features}} </p>
              <label>Owner</label>
              <p> {{card.owner}} </p>
              <label>Product Home Page</label>
              <p> {{card.product_homepage}} </p>
          </b-collapse>
        </b-card-text>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import {EventBus} from "../../index.js";

export default {
  data() {return {
    cards : [],
    search : ''
  }
 },
  beforeMount() {
    const self = this;
    var get_url = "/api/product-table";

    axios.get(get_url)
    .then(response => {
      self.cards = response.data
    }
    )
    .catch(error => console.log(error))
  },
  methods:{
    OpenDetail(id) {
      EventBus.$emit('product-selection-changed' ,this.selectedRow = id)
    },

    toggleSearch(value) {
      if ( this.search != value){
        this.search = value
      }
      else {
        this.search = ''
      }
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

<style lang="css" scoped>

.card{
  border: 0px;
  border-top-style: solid;
  border-top-width: medium;
  border-image: linear-gradient(to right,#7799FF,purple) 1;
  box-shadow:
    -8px -8px 8px 0 rgba(255,255,255,0.5),
    8px 8px 8px 0 rgba(0,0,0,0.05);
}

</style>
