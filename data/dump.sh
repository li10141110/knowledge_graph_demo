
# dump into neo4j
neo4j-import --into [your-path-to-database]/kgDemo --nodes person_node.txt --nodes company_node.txt --relationships management_edge.txt --delimiter TAB

# dump into mysql
mysql -u root -p[your-password] < dump.sql


