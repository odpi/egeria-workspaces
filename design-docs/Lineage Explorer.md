The lineage explorer is a new card on the portal.  It may also be linked to from other cards (details below).

The lineage explorer centres around an asset.  This is called the focus asset.  Its identifier is either passed as a guid from another part of the portal (the catalog's infrastructure assets, data assets, APIs, processes, or egeria-explorer's data sets found as part of digital products in the digital product catalog) or the user is given an option to find/select an asset, (AssetMaker.find_asset, graph_query_depth=0).

The first step is to retrieve the basic asset graphs with AssetCatalog.get_asset_graph(guid).  This call has an option called as_of_time which requests that the lineage is returned for the requested point in time.  The first time that AssetCatalog.get_asset_graph(guid) is called, as_of_time is set to null which means "now".  The results of this first call are used to set up the start and end dates of a time slider.  The start date is the createTime from the asset element header,  and the endTime is "now".  The default position of the slider is "now".  If the user moves the slider, the position of the slider is used to set as_of_time and the AssetCatalog.get_asset_graph(guid) call is refreshed.  This allows the user to query how the lineage is changing over time.

The results of AssetCatalog.get_asset_graph(guid) are used to display the asset guid and properties returned.
There are also the following lineage graphs that can be extracted from the results of AssetCatalog.get_asset_graph.  Any one of them may be null.  If available, the local lineage graph should always be displayed and the field level lineage graph should be optionally displayed at the user's request.

- Local Lineage Graph (key localLineageGraph) - this graph shows the elements directly connected by lineage relationships.  These relationships are accessed by the lineageLinkage key in the response.  They should be listed below this graph in a table showing the relationship guid, relationship label, relationship description, related element display name, related element description, and type of the related element.  Also,  if the related element is an asset (check in elementHeader for type name == "Asset" or super type name contains "ASSET" ) allowing the user to click a button and the element becomes the focus asset - and the page is refreshed for this element and as_of_time setting.
- Field-Level Lineage Graph (key fieldLevelLineageGraph) - This graph shows the mapping for data fields from one lineage linked asset to another.

The response key partOfInformationSupplyChains may optionally contain a list of information supply chains that the asset belongs to.  These elements should be displayed in a table showing qualifiedName, display name, description. There should also be a view button to take the user to the information supply chain in egeria-explorer.  Also, the user should be able to optionally select one of these information supply chains to use on the AssetCatalog.get_asset_lineage_graph() described below.

If the local lineage graph is not null then the following lineage graphs can also be retrieved using AssetCatalog.get_asset_lineage_graph().  These graphs should be optionally displayed at the user's request.  If either/both of these graphs is displayed, then the AssetCatalog.get_asset_lineage_graph() is refreshed each time the slider is moved by the user.

- Full Asset Lineage Graph (key is mermaidGraph or fullLineageMermaidGraph) - this shows the end to end flow of data and control across the IT landscape through the asset.
- Edge Asset Lineage Graph (edgeMermaidGraph) - this shows the elements at the extreme edges of the full lineage graph - linked to the focus asset.  It is useful for very large lineage graphs to see the ultimate sources and destinations of the data.

There are a number of options that the user should be able to select to control the lineage graph content from AssetCatalog.get_asset_lineage_graph():

- If they have selected an information supply chain (described above), they can choose to either limit the display to a single information supply chain (pass the information supply chain qualified name on the limitToISCQualifiedName option) or highlight the information supply chain (pass the information supply chain qualified name on the highlightISCQualifiedName option)
- The allAnchors boolean option controls wither the field level detail is shown.

The output of the AssetCatalog.get_asset_lineage_graph() request is the two asset lineage graphs plus a table of the nodes on the graph (see linkedAssets key).  This table should show the displayName, description, guid, qualifiedName, create time and last update time (updateTime).  The createTime and updateTime are in the element header with the guid.

Please add descriptions of each graph and table to the display.

Note: the slider feature and the use of as_of_time is expected to be a common feature that is added to each page of egeria_explorer and the catalog in the portal.