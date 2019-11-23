

<template>
  <div class="conatainer-fluid">
    <b-card class="mt-3" header="Form Data Result">
      <pre class="m-0">{{ form }}</pre>
    </b-card>
    <h1>Detail</h1>
    <b-form id='personaDetails'
    @edit="onEdit">
      <div>
        <label for="Name">Name</label>
        <b-form-input v-model="form.name"  name="Name" />
      </div>
      <div>
        <label for="Title">Title</label>
        <b-form-input v-model="form.title" id="Title" name="Title" />
      </div>
      <div>
        <label for="external">Internal or External?</label>
        <b-form-radio v-model="form.external" name="some-radios"
        value="1">External</b-form-radio>
        <b-form-radio v-model="form.external" name="some-radios"
        value="0">Internal</b-form-radio>
      </div>
      <div>
        <label for="qty">Number people who fit this persona</label>
        <b-form-input type="number" v-model="form.qty" id="qty" name="qty" />
      </div>
      <div>
        <label for="quote">Persona Quote</label>
        <b-form-textarea v-model="form.quote" id="quote" name="quote" />
      </div>
      <div>
        <label for="function">Job Function</label>
        <b-form-textarea v-model="form.jobFunction" id="function" name="function" />
      </div>
      <div>
        <label for="needs">Needs</label>
        <b-form-textarea v-model="form.needs" id="needs" name="needs" />
      </div>
      <div>
        <label for="wants">Wants</label>
        <b-form-textarea v-model="form.wants" id="wants" name="wants" />
      </div>
      <div>
        <label for="pain_point">Pain Points</label>
        <b-form-textarea v-model="form.pain_point" id="pain_point" name="pain_point" />
      </div>
      <div>
        <label for="buss_val">value to business</label>
        <b-form-input type="range" min="0" max="5" v-model="form.buss_val" />
      </div>
      <div>
        <label for="persona_file">Add File</label>
        <b-form-file v-model="form.persona_file"
        :state="Boolean(form.persona_file)"
        name="persona_file"
        placeholder="Choose a file or drop it here..."
        drop-placeholder="Drop file here..."></b-form-file>
      </div>

      <b-button type="edit" variant="primary">Edit</b-button>
  </b-form>
</div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import {EventBus} from "../event-bus.js";

export default {
  name: "personaDetails",
  data() {
    return {
      form: {
        name: '',
        title: '',
        external: '',
        qty: '',
        quote: '',
        jobFunction: '',
        needs: '',
        wants: '',
        pain_point: '',
        buss_val: '',
        persona_file: null},
        show: true
      }
    },
    beforeMount() {
      const self = this;
      EventBus.$on('selection-changed', function(selection){
        console.log(`this is the row I selected: ${selection}`)

        var get_url = "http://localhost:5000/api/persona-table/";
        get_url += selection;

        axios.get(get_url)
        .then(response => {
            self.form = response.data[0];
            self.form.name = response.data[0].name;
            console.log(response.data[0]);
          }
        )
        .catch(error => console.log(error))
        });
      },
      methods: {
        onEdit(evt) {//TODO: Route},
        },
      },
  };

</script>
