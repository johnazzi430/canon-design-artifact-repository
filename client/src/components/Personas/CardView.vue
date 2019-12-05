

<template lang="html">
  <div class="container" style="margin-top:0px">
    <div class="md-form mt-0" id="card-search">
      <input v-model="search"
        class="form-control"
        type="text"
        placeholder="Search for user persona"
        aria-label="Search">
    </div>
    <br>

    <b-card-group columns>
      <b-card class="card" v-for="card in cards" v-bind:key="card.id">
        <div class="col">
                  <img src="../../../public/assets/img_avatar2.png" alt="Avatar" class="avatar">
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
    cards : {},
    search : ''
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
      EventBus.$emit('selection-changed' ,this.selectedRow = id)
    },
  },
};

</script>

<style lang="css" scoped>
.avatar {
  display: block;
  margin-left: auto;
  margin-right: auto;
  min-width: 50px;
  max-width: 50px;
  min-height: 50px;
  max-height: 50px;
  border-radius: 50%;
};

</style>
