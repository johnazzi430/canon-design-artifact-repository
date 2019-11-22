Title

<template>
  <div class="col-6">

    <h1>Add </h1>"
    <b-form
              @submit="onSubmit"
              @reset="onReset"
              v-if="show">
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
        <b-form-radio v-model="form.external" name="some-radios" value="1">External</b-form-radio>
        <b-form-radio v-model="form.external" name="some-radios" value="0">Internal</b-form-radio>
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

      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    <b-card class="mt-3" header="Form Data Result">
      <pre class="m-0">{{ form }}</pre>
    </b-card>
  </div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'

export default {
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
    methods: {
     onSubmit(evt) {
       evt.preventDefault()
       axios({
           method: 'post',
           url: 'http://localhost:5000/api/persona-table',
           data: this.form,
       })
       .then(function (response) {
           console.log(response);
       })
       .catch(function (error) {
           console.log(error);
       })
      alert("form submitted" + JSON.stringify(this.form))
     },

     onReset(evt) {
       evt.preventDefault()
       // Reset our form values
       this.form.name = ''
       this.form.title = ''
       this.form.external = ''
       this.form.qty = ''
       this.form.quote = ''
       this.form.jobFunction = ''
       this.form.needs = ''
       this.form.wants = ''
       this.form.pain_point = ''
       this.form.buss_val = ''
       this.form.persona_file = null
     },
   },
 };

</script>


<!--
<div>{{ form.name.label }}: {{ form.name}}</div>
<div>{{ form.title.label }}: {{ form.title}}</div>
<div>{{ form.quote.label }}: {{ form.quote}}</div>
<div>{{ form.function.label }}: {{ form.function}}</div>
<div>{{ form.needs.label }}: {{ form.needs}}</div>
<div>{{ form.wants.label }}: {{ form.wants}}</div>
<div>{{ form.pain_point.label }}: {{ form.pain_point}}</div>
<div>{{ form.persona_file.label }}: {{ form.persona_file}}</div>
<div>  {{ form.submit }}</div>
  {{ form.csrf_token }}
-->
