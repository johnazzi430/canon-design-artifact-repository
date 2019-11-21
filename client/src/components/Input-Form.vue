

<template>
  <form method="POST" action="/input-form" >

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
  </form>

<template>
