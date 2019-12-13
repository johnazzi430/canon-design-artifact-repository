

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
      <b-card class="card" v-for="card in filterItems(cards)" v-bind:key="card.name">
        <b-card-text>
          <p class="well">
            {{card.title}}
          </p>
          <b-button v-b-toggle="'collapse-'+card.id"
            variant="outline-secondary">More Detail</b-button>
               <!-- class="stretched-link " -->
          <b-button href="javascript:void(0)" v-on:click = 'OpenDetail(card.id)'
              variant="outline-secondary">Open insight</b-button>
          <b-collapse :id="'collapse-'+card.id" class="mt-2">
              <label for="function">Description</label>
              <p class="text-wrap"> {{card.description}} </p>
              <label style="white-space: pre-line;">Experience Vector</label>
              <p> {{card.experience_vector}} </p>
              <label  style="white-space: pre-line;">Journey</label>
              <p> {{card.journey}} </p>
              <label>Emotions</label>
                <p> {{card.emotions}} </p>
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
    cards : {},
    search : ''
  }
 },
  beforeMount() {
    const self = this;
    var get_url = `/api/insights`;

    axios.get(get_url)
    .then(response => {
      self.cards = response.data
    }
    )
    .catch(error => console.log(error))
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

</style>
