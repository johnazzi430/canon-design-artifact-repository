<template>
  <div class="container">
    <h1>Roles Page</h1>
    <div class="test-header row" style="margin:15px">
      <div class="col-2">
        Selection:
        <span id="selectedRows"></span>
        <span :selectedRow = "selectedRow"></span>
      </div>
      <div class="col-2">
        <span> Search: </span>
        <input type="text" id="filter-text-box"
        placeholder="Filter..." v-on:input="onFilterTextBoxChanged()"/>
      </div>
    </div>
    <ag-grid-vue style="width: 100vl; height: 500px;"
        class="ag-theme-balham"
        :columnDefs="columnDefs"
        :rowData="rowData"
        :modules="modules"
        rowSelection="single"
        @grid-ready="onGridReady"
        @selection-changed="onSelectionChanged"
        @cell-value-changed="onCellValueChanged">
  </ag-grid-vue>
</div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import {AgGridVue} from "@ag-grid-community/vue";
import {AllCommunityModules} from '@ag-grid-community/all-modules';
import store from  "../../store";

export default {
  name: 'roles',
  data() {
    return {
      columnDefs: null,
      rowData: null,
      rowSelection: null,
      gridApi: null,
      gridOptions: null,
      modules: AllCommunityModules,
      selectedRow: null,
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

    onSelectionChanged() {
      var selectedRows = this.gridApi.getSelectedRows();
      var selectedRowsString = "";
      var selectedRowsid =""
      selectedRows.forEach(function(selectedRow, index) {
        if (index !== 0) {
          selectedRowsString += ", ";
        }
        selectedRowsString += selectedRow.name;
        selectedRowsid = selectedRow.id
      });

      document.querySelector("#selectedRows").innerHTML = selectedRowsString;
    },

    onFilterTextBoxChanged() {
      this.gridApi.setQuickFilter(document.getElementById('filter-text-box').value);
    },


    // async onCellValueChanged(params) {
    //   // var colId = params.column.getId();
    //   console.log( params.data.username,params.data.role)
    //   await axios({
    //      method: 'put',
    //      url: '/api/users/' + params.data.user_id,
    //      data: {
    //        'role': params.data.role
    //      }
    //   })
    // },

  },
  beforeMount() {
    this.columnDefs = [
      {headerName: "Rolee", field: "role", filter: 'agTextColumnFilter', width: 200},
      {headerName: "Description", field: "name",
          filter: 'agTextColumnFilter', width: 400, editable:true},
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
    fetch('/api//persona/roles')
    .then(result => result.json())
    .then(rowData => this.rowData = rowData);
  },
};


</script>
