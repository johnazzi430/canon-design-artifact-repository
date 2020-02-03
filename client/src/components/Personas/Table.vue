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
    <ag-grid-vue style="width: 100vl; height: 100vh;"
        class="ag-theme-material"
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

  beforeMount() {

    this.defaultColDef = {
      sortable: true,
      resizable: true,
      getQuickFilterText: function(params) {
        return params.value.name;
      }
    };

    this.getRowHeight = params => {
      return params.data.rowHeight;
    };

    this.gridOptions = {enableBrowserTooltips: true};
    this.rowSelection = "single";
    this.rowHeight = 50;

    this.columnDefs = [
      {headerName: "Title", field: "title", filter: 'agTextColumnFilter', width: 200 , resizable: true , sortable: true , cellClass: "cell-wrap-text",},
      {headerName: "Quote", field: "quote", filter: 'agTextColumnFilter', width: 400 , resizable: true , sortable: true, cellClass: "cell-wrap-text",},
      {headerName: "    ", field: "external" ,  width: 50 , headerTooltip:'External Persona', filter: 'agNumberColumnFilter', resizable: true , sortable: true, cellRenderer: externalFlag},
      {headerName: "Function", field: "job_function", filter: 'agTextColumnFilter', width: 400 , resizable: true , sortable: true},
      {headerName: "    ", field: "market_size", headerTooltip:'Market Size' , width: 75 , resizable: true , sortable: true},
      {headerName: "Roles", field: "roles", filter: 'agTextColumnFilter' , flex: 2, resizable: true , sortable: true , cellRenderer: roleBadge , cellClass: "cell-wrap-text",  minWidth: 200, maxWidth: 350},
    ];


    fetch(`/api/persona-table`)
    .then(result => result.json())
    .then(rowData => this.rowData = rowData);

    this.$nextTick(() => {
        fetch(`/api/persona-table`)
        .then(result => result.json())
        .then(rowData => this.rowData = rowData);
    });
  },
  mounted() {
    this.gridApi = this.gridOptions.api;
    this.gridColumnApi = this.gridOptions.columnApi;

    api.sizeColumnsToFit()

    const self = this

    EventBus.$on('persona-table-changed',function(data) {
      fetch(`/api/persona-table`)
      .then(result => result.json())
      .then(rowData => self.rowData = rowData);
        console.log('recived')
    })
  },
  methods: {
    onGridReady(params) {
      this.gridApi = params.api;
      this.columnApi = params.columnApi;
      this.rowHeight = 200;

      try {
          params.api.context.beanWrappers.tooltipManager.beanInstance.MOUSEOVER_SHOW_TOOLTIP_TIMEOUT = 0;
        } catch (e) {
          console.error(e);
        }
    },

    onColumnResized() {
      this.gridApi.resetRowHeights();
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
      this.$router.push('/persona/' + selectedRowsid )
    },


    onFilterTextBoxChanged() {
      this.gridApi.setQuickFilter(document.getElementById('filter-text-box').value);
    },
  },
};

function externalFlag(params) {
  if (params.value === 1) {
    return '<i class="fas fa-external-link-square-alt"></i>'
  }
  else {
    return ''
  };
};

function roleBadge(params) {
  var out = ''
  params.value.forEach((item,index) => {
    out = out + '<div class="badge badge-primary">'+ item.name + '</div>'
  })
//  return  '<i class="fas fa-external-link-square-alt"></i>'
  return '<div>' + out + '</div>'
};

</script>

<style lang="scss" scoped>
.cell-wrap-text {
    white-space: normal !important;
}
</style>
