

<template lang="html">
  <div class="container" style="margin-top:0px">
    <div class="row ">
      <div class="md-form mt-0 col-8" id="card-search">
        <input v-model="search"
          class="form-control"
          type="text"
          placeholder="Search for user persona"
          aria-label="Search">
      </div>
      <h4>Filter:</h4>
      <b-button-group class="mx-1">
        <b-button variant="info" @click='toggleSearch(`"external":0`)'>Internal</b-button>
        <b-button variant="info" @click='toggleSearch(`"external":1`)'>External</b-button>
      </b-button-group>
    </div>
    <br>

    <b-card-group columns>
      <b-card class="card" v-for="card in SearchItems(cards)" v-bind:key="card.id">
        <div>
          <div>
            <div v-if="card.avatar == true">
              <img
               v-bind:src="'/api/persona/avatar/' + card.id"
               class="avatar">
            </div>
            <div v-else>
                <img src="../../../public/assets/img_avatar2.png"
                     alt="Avatar" class="avatar">
            </div>
          </div>
        </div>
        <b-card-text>
          <span> {{card.name}} the {{card.title}}
          </span>
          <p class="well">
            {{card.quote}}
          </p>
          <b-button v-b-toggle="'collapse-'+card.id"
            variant="outline-secondary">More Detail</b-button>
               <!-- class="stretched-link " -->
          <b-button href="javascript:void(0)" v-on:click = 'OpenDetail(card.id)'
              variant="outline-secondary">Open Persona</b-button>
          <b-collapse :id="'collapse-'+card.id" class="mt-2">
              <label for="function">Job Function</label>
              <p class="text-wrap"> {{card.job_function}} </p>
              <label for="needs" style="white-space: pre-line;">Needs</label>
              <p> {{card.needs}} </p>
              <label for="wants" style="white-space: pre-line;">Wants</label>
              <p> {{card.wants}} </p>
              <label for="pain_point">Pain Points</label>
                <p> {{card.pain_point}} </p>
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
    search : '',
    filter : ''
  }
 },
  beforeMount() {
    const self = this;
    var get_url = `/api/persona-table`;

    axios.get(get_url)
    .then(response => {
      self.cards = response.data
    }
    )
    .catch(error => console.log(error))
  },
  methods:{
    OpenDetail(id) {
      EventBus.$emit('persona-selection-changed' ,this.selectedRow = id)
      this.$router.push('/persona/' + id )
    },

    toggleSearch(value) {
      if ( this.search != value){
        this.search = value
      }
      else {
        this.search = ''
      }
    },

    SearchItems: function(cards) {
      var self = this;
      return cards.filter(function(cards) {
        let regex = new RegExp('(' + self.search+ ')', 'i');
//        return cards.name.match(regex);
        return JSON.stringify(cards).match(regex);
      })
    },

  },
};

</script>

<style lang="scss" scoped>

.avatar {
  width: 50px;
  height: 50px;
  display: block;
  object-fit: cover;
  margin-left: auto;
  margin-right: auto;
  border-radius: 50%;
}

.card {
  border-radius: 10px;
  box-shadow:
    -8px -8px 8px 0 rgba(255,255,255,0.4),
    8px 8px 8px 0 rgba(0,0,0,0.05);
}

</style>
