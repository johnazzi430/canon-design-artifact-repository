<template>
  <div class="container">
    <h1>Admin Page</h1>

    <div class="test-header row" style="margin:15px">
      <div class="col-4">
        Selection:
        <span>{{selectedRows[0]}}</span>
        <br>
        <a href="javascript:void(0)"
           v-on:click="resetPasswordforUser(selectedRows)">Reset Password</a>
      </div>
      <div class="col-2">
        <span> Search: </span>
        <input type="text" id="filter-text-box"
        placeholder="Filter..." v-on:input="onFilterTextBoxChanged()"/>
      </div>
    </div>
    <ag-grid-vue style="width: 100vl; height: 500px;"
        class="ag-theme-material"
        :columnDefs="columnDefs"
        :rowData="rowData"
        :modules="modules"
        rowSelection="single"
        @selection-changed="onSelectionChanged"
        @grid-ready="onGridReady"
        @cell-value-changed="onCellValueChanged">
  </ag-grid-vue>
</div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import {AgGridVue} from "@ag-grid-community/vue";
import {AllCommunityModules} from '@ag-grid-community/all-modules';
import {EventBus} from "../../index.js";
import store from  "../../store";

export default {
  name: 'ProductTable',
  data() {
    return {
      columnDefs: null,
      rowData: null,
      rowSelection: null,
      selectedRows: [],
      gridApi: null,
      gridOptions: null,
      modules: AllCommunityModules,
      defaultColDef: null
    }
  },
  components: {
    AgGridVue
  },
  methods: {
    onGridReady(params) {
      this.gridApi = params.api;
      this.columnApi = params.columnApi;
    },

    onFilterTextBoxChanged() {
      this.gridApi.setQuickFilter(document.getElementById('filter-text-box').value);
    },

    async onCellValueChanged(params) {
      // var colId = params.column.getId();
      console.log( params.data.username,params.data.role)
      await axios({
         method: 'put',
         url: '/api/users/' + params.data.user_id,
         data: {
           'role': params.data.role
         }
      })
    },

    onSelectionChanged() {
      this.selectedRows = this.gridApi.getSelectedRows();
    },

    resetPasswordforUser(params){
      console.log(params[0].user_id)
      axios({
         method: 'put',
         url: '/api/users/' + params[0].user_id + '/password-reset',
       })
       this.$store.commit({
         type: 'alert',
         show : 5,           //seconds to auto dismiss
         variant : "success",
         content : params[0].username + " password updated"
       })
     },

  },
  beforeMount() {
    this.columnDefs = [
      {headerName: "User ID", field: "user_id", width: 75},
      {headerName: "Username", field: "username", filter: 'agTextColumnFilter', width: 200},
      {headerName: "Role", field: "role", filter: 'agTextColumnFilter', width: 100, editable:true},
      // {headerName: "blank"  , cellRenderer: resetPassword}
    ];

    this.defaultColDef = {
      sortable: true,
      resizable: true,
      filter: true,
      getQuickFilterText: function(params) {
        return params.value.name;
      }
    };

    this.gridOptions = {};
    this.rowSelection = "single";
    this.gridOptions.rowHeight = 100;
    fetch('/api/users')
    .then(result => result.json())
    .then(rowData => this.rowData = rowData);
  },
  mounted() {
    const self = this

  },
};

function resetPassword(params) {
  return '<a href="javascript:void(0)" v-on:click="resetPasswordforUser">Reset Password</a>'
};


</script>
