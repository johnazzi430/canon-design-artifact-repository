<template>
  <div>
    <div class="test-header row" style="margin:15px;">
      <b-alert :show="this.alert_show === true" variant="info" dismissible>
        Data Updated {{this.alert_text }}
    </b-alert>
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
    <ag-grid-vue style="width: 100%; height: 100vh;"
        class="ag-theme-balham"
        :columnDefs="columnDefs"
        :rowData="rowData"
        :modules="modules"
        rowSelection="single"
        @grid-ready="onGridReady"
        @selection-changed="onSelectionChanged">
  </ag-grid-vue>
</div>
</template>

<script>
/*eslint-disable */
import {AgGridVue} from "@ag-grid-community/vue";
import {AllCommunityModules} from '@ag-grid-community/all-modules';
import {EventBus} from "../../index.js";


const API_URL = process.env.API_URL

export default {
  name: 'PersonaTable',
  data() {
    return {
      columnDefs: null,
      rowData: null,
      rowSelection: null,
      gridApi: null,
      gridOptions: null,
      modules: AllCommunityModules,
      selectedRow: null,
      defaultColDef: null,
      alert_show: false,
      alert_text: null,
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
      EventBus.$emit('persona-selection-changed' ,this.selectedRow = selectedRowsid)
    },


    onFilterTextBoxChanged() {
      this.gridApi.setQuickFilter(document.getElementById('filter-text-box').value);
    },
  },

  mounted() {
    const self = this

    EventBus.$on('persona-changed',function(data) {
      fetch(`/api/persona`)
      .then(result => result.json())
      .then(rowData => self.rowData = rowData);
        console.log('recived')
    })
  },

  beforeMount() {

    this.columnDefs = [
      {headerName: "Title", field: "title", filter: 'agTextColumnFilter', width: 200},
      {headerName: "Quote", field: "quote", filter: 'agTextColumnFilter', width: 400},
      {headerName: "Internal or External", field: "external" ,  width: 50 , headerTooltip:'Flag if external', filter: true},
      {headerName: "Function", field: "job_function", filter: 'agTextColumnFilter', width: 400},
      {headerName: "Market Size", field: "market_size", filter: true, width: 50},
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
    this.gridOptions.rowHeight = 200;
    fetch(`/api/persona`)
    .then(result => result.json())
    .then(rowData => this.rowData = rowData);

    this.$nextTick(() => {
        fetch(`/api/persona`)
        .then(result => result.json())
        .then(rowData => this.rowData = rowData);
    });
  },
};


    var externalCellRender = function(params) {
        return '<span style="color: '+params.color+'">' + params.value + '</span>';
    }

</script>

<style>
</style>
