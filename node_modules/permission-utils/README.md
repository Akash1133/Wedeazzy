# permission-utils
A set of useful functions for managing group-based permissions.
## Features:

* DB-agnostic because it assumes you've already retrieved the relevant info to pass in
* Framework-agnostic because it just gives you back an object that specifies all permissions for the given user and you can decide what to do with that info
* Can handle whitelisted group permissions or blacklisted.
* Lightweight
* Has zero package dependencies
* Includes a static html page to help you build your whitelist/blacklist (see https://andrewfulrich.github.io/permission-utils/permsko.html)
* Runs off json files to specify which "tables" (really could be any resource/collection if you are using nosql) give/revoke which CRUD permissions to which groups.

These json files look like this:
```
{
    "table1": {
        "group1":{"c":true,"r":true,"u":false,"d":false},
        "group2":{"c":false,"r":true,"u":true,"d":false}
    },
    "table2":{}
}
```
For `table1` in the above json, if this were specified as a whitelist, it would grant:

 * create, read, and update to a user who belonged to both group1 and group2
 * create and read to a user who belonged to group1
 * read and update to a user who belonged to group2
 * no permissions to a user who belonged to neither

If this were specified as a blacklist, it would grant:

 * read only to a user who belonged to both group1 and group2
 * create and read to a user who belonged to group1
 * read and update to a user who belonged to group2
 * all permissions to a user who belonged to neither

## To Use

To use, pass the required info into getGroupPerms to get the user's permissions.
For example, for a user who belongs to both group1 and group2 for the above whitelist, the output will look like so:
```
{
    "table1":{ "c":true,"r":true","u":true,"d":false },
    "table2":{ "c":false,"r":false","u":false,"d":false }
}
```

You can then use those results to allow/disallow the user to perform the actions specified as you see fit (these utils don't help you with that part).

If you also have a blacklist that you want to use to determine permissions, run the blacklist through that function too, then combine the results using the combineWhiteAndBlackResults function.

For detailed API documentation, see https://andrewfulrich.github.io/permission-utils/

Here's an example that creates a middleware for express.js to attach permissions to a user based on their groups:
```
const whitelist = require('../whitelist.json')
const blacklist = require('../blacklist.json')
const permUtils = require('permission-utils')

module.exports = (pgQuery)=> {
  async function getPerms(userId) {
    let result = await pgQuery({
      text:'select g.name from SCHEMA.group g INNER JOIN SCHEMA.user_group ug ON ug.group_id=g.id INNER JOIN SCHEMA.user u ON u.id=ug.user_id WHERE u.id=$1',
      values:[userId]
    })
    let userGroups=result.rows.map(row=>row.name)
    let whiteResults=permUtils.getGroupPerms(userGroups,whitelist)
    let blackResults=permUtils.getGroupPerms(userGroups,blacklist,true)
    if(Object.keys(whitelist) && Object.keys(blacklist)) {
      return Promise.resolve(permUtils.combineWhiteAndBlackResults(whiteResults,blackResults));
    } else if(Object.keys(blacklist)) {
      return Promise.resolve(blackResults)
    }  else { //covers both whitelist is blank and whitelist isn't blank
      return Promise.resolve(whiteResults)
    }
  }
  async function userPermMiddleware(req,res,next) {
    if(req.user && req.user.id) {
      req.user.perms = await getPerms(req.user.id)
      next()
    } else {
      next()
    }
  }
  return userPermMiddleware
}
```