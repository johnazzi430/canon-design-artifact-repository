<template>
  <div>
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
    <ag-grid-vue style="width: 100vl; height: 100vh;"
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

export default {
  name: 'ProductTable',
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
      EventBus.$emit('product-selection-changed' ,this.selectedRow = selectedRowsid)
      this.$router.push('/product/' + selectedRowsid )
    },

    onFilterTextBoxChanged() {
      this.gridApi.setQuickFilter(document.getElementById('filter-text-box').value);
    },

  },
  beforeMount() {
    this.columnDefs = [
      {headerName: "Name", field: "name", width: 200},
      {headerName: "Description", field: "description", filter: 'agTextColumnFilter', width: 200},
      {headerName: "Goals", field: "goals", filter: 'agTextColumnFilter', width: 400},
      {headerName: "Features", field: "features", filter: 'agTextColumnFilter', width: 400},
      {headerName: "Owner", field: "owner", filter: true, width: 50},
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
    fetch('/api/product-table')
    .then(result => result.json())
    .then(rowData => this.rowData = rowData);
  },
  mounted() {
    const self = this

    EventBus.$on('product-table-changed',function(data) {
      fetch(`/api/product-table`)
      .then(result => result.json())
      .then(rowData => self.rowData = rowData);
    })
  },
};


    var externalCellRender = function(params) {
        return '<span style="color: '+params.color+'">' + params.value + '</span>';
    }

</script>
