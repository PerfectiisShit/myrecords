# myrecords: Operate mysql simply 
Operate mysql database with python objects, this is based on kennethreitz/records project


☤ Basic Usages
----------
Operate your mysql database with python objects instead of sql strings, here are some examples:  

**Select data**


<pre>
    from records import SimpleMysql as SM

    sm = SM("mysql://test:test@localhost/Test")
    table = "tickets"
    condition = {'eid': '79', 'ticnum': ['like', 'NETWK%']}
    rs = sm.select(table=table, condition=condition, limit=10, order_by='nid', order_direction='DESC')
    
    >>> print(rs.dataset)
    eid|nid|tid |cid|status   |ticnum       |title                      |requester|local_only
    ---|---|----|---|---------|-------------|---------------------------|---------|----------
    79 |10 |    |   |Finished |NETWK32570338|03/19 Vendor CenturyLink   |jiahong  |0
    ...
    79 |3  |    |   |Finished |NETWK32570273|03/19 Vendor CenturyLink   |jiahong  |0
    79 |2  |    |   |Submitted|NETWK32570265|03/19 Vendor CenturyLink   |jiahong  |0
    79 |1  |    |   |Submitted|NETWK32570250|03/19 Vendor CenturyLink   |jiahong  |0
</pre>


**Insert data**  

<pre>
    insert_content = {'eid': '79', 'requester': 'somebody', 'ticnum': 'NETWKTEST1234', 'Title': 'This is a test row', 'local_only': '0'}
    sm.insert(table=table, content=insert_content)
    rs = sm.select(table=table, condition=condition, limit=10, order_by='nid', order_direction='DESC')
    
    >>> print(rs.dataset)
    eid|nid |tid |cid |status   |ticnum       |title                      |requester|local_only
    ---|----|----|----|---------|-------------|---------------------------|---------|----------
    79 |2584|    |    |         |NETWKTEST1234|This is a test row         |somebody |0
    ...
    79 |3   |    |    |Finished |NETWK32570273|03/19 Vendor CenturyLink   |jiahong  |0
    79 |2   |    |    |Submitted|NETWK32570265|03/19 Vendor CenturyLink   |jiahong  |0
    79 |1   |    |    |Submitted|NETWK32570250|03/19 Vendor CenturyLink   |jiahong  |0
 </pre>   


**Update data**  

<pre>
    update_content = {'status': 'Finished'}
    update_condition = {'nid': '2584'}
    sm.update(table=table, content=update_content, condition=update_condition)
    rs = sm.select(table=table, condition=condition, order_by='nid', order_direction='DESC')
    
    >>> print(rs.dataset)
    eid|nid |tid |cid |status   |ticnum       |title                      |requester|local_only
    ---|----|----|----|---------|-------------|---------------------------|---------|----------
    79 |2584|    |    |Finished |NETWKTEST1234|This is a test row         |somebody |0
    ...
    79 |3   |    |    |Finished |NETWK32570273|03/19 Vendor CenturyLink   |jiahong  |0
    79 |2   |    |    |Submitted|NETWK32570265|03/19 Vendor CenturyLink   |jiahong  |0
    79 |1   |    |    |Submitted|NETWK32570250|03/19 Vendor CenturyLink   |jiahong  |0
</pre>    


**Delete data**  

<pre>
    delete_condition = {'nid': '2584'}
    sm.delete(table=table, condition=delete_condition)
    rs = sm.select(table=table, condition=condition, limit=10, order_by='nid', order_direction='DESC')
    
    >>> print(rs.dataset)
    eid|nid|tid |cid|status   |ticnum       |title                      |requester|local_only
    ---|---|----|---|---------|-------------|---------------------------|---------|----------
    79 |10 |    |   |Finished |NETWK32570338|03/19 Vendor CenturyLink   |jiahong  |0
    ...
    79 |3  |    |   |Finished |NETWK32570273|03/19 Vendor CenturyLink   |jiahong  |0
    79 |2  |    |   |Submitted|NETWK32570265|03/19 Vendor CenturyLink   |jiahong  |0
    79 |1  |    |   |Submitted|NETWK32570250|03/19 Vendor CenturyLink   |jiahong  |0
    ...
</pre>


☤ Tips
-----------
This project can only be used to operate mysql database, for more powerful functions, go check [kennethreitz/records](<https://github.com/kennethreitz/records>) project
