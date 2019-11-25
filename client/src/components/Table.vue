<template>
    <div>
      <div class="test-header">
            Selection:
              <span id="selectedRows"></span>
              <span :selectedRow = "selectedRow"></span>
      </div>
      <ag-grid-vue style="width: 100%; height: 500px;"
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
    import {EventBus} from "../event-bus.js";

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
                selectedRow:null
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
                          EventBus.$emit('selection-changed' ,this.selectedRow = selectedRowsid)
                        },
                },
        beforeMount() {
          this.columnDefs = [
            {headerName: "Name", field: "name", filter: 'agTextColumnFilter', width: 200},
            {headerName: "Title", field: "title", filter: 'agTextColumnFilter', width: 200},
            {headerName: "Quote", field: "quote", filter: 'agTextColumnFilter', width: 200},
            {headerName: "Internal or External", field: "external" ,  width: 50 , headerTooltip:'Flag if external', filter: true},
            {headerName: "Function", field: "job_function", filter: 'agTextColumnFilter', width: 200},
            {headerName: "Market Size", field: "market_size", filter: true, width: 50},

          ];
          this.rowSelection = "single";
          fetch('http://localhost:5000/api/persona-table')
                          .then(result => result.json())
                          .then(rowData => this.rowData = rowData);
        },
    }

    var externalCellRender = function(params) {
        return '<span style="color: '+params.color+'">' + params.value + '</span>';
    }

</script>

<style>
</style>
