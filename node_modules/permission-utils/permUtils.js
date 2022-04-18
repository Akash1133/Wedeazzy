/**
 Permission Utils

 A set of useful functions for managing group-based permissions.

 Author: Andrew Ulrich

 MIT License

 Copyright (c) 2017 Andrew F. Ulrich

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
 */

/**
 * Get the permissions of a given user based on the groups he/she belongs to
 * @param groups an array of the groups the user belongs to
 * @param permSpecs a json object specifying which permissions to grant for which groups on which resources (see test files for examples)
 * @param isBlackList whether or not the permSpecs are a blacklist, defaults to false (a whitelist)
 * @returns {*} an object with tables for keys and CRUD permissions for values (e.g. {c:false,r:true,u:false,d:false} == read only)
 */
function getGroupPerms(groups,permSpecs,isBlackList=false) {
  return Object.keys(permSpecs)
    .reduce((accum,table)=>Object.assign(accum,{[table]:
      {
        c:hasPerm(table,groups,'c',permSpecs,isBlackList),
        r:hasPerm(table,groups,'r',permSpecs,isBlackList),
        u:hasPerm(table,groups,'u',permSpecs,isBlackList),
        d:hasPerm(table,groups,'d',permSpecs,isBlackList)
      }}),{})
}

/**
 * check to see if the groups that the user is in grants him/her permission to do the given action on the given resource
 * @param table the table/resource upon which the action would be performed
 * @param groups and array of group names
 * @param action String can be 'c', 'r', 'u', or 'd'
 * @param permSpecs the permission specifications
 * @returns {boolean}
 */
function hasPerm(table,groups,action,permSpecs,isBlackList=false) {
  if(!permSpecs[table]) return isBlackList; //if there are no perms specified for that table, then give no perms for it if whitelist or all perms if blacklist
  let relevantGroups=Object.keys(permSpecs[table]).filter(group=>groups.includes(group))
  if(relevantGroups.length == 0) return isBlackList; //user is not in any group that specified permissions, so give no perms if whitelist, all if black
  if(isBlackList) {
    return !relevantGroups.some(group=>!permSpecs[table][group][action])
  } else {
    return relevantGroups.some(group=>permSpecs[table][group][action])
  }
}

/**
 * invert the given permissions
 * @param userPerms this is the output from getGroupPerms
 */
function invertResults(userPerms) {
  return Object.keys(userPerms).reduce((tables,table)=>
    Object.assign(tables,{[table]:Object.keys(userPerms[table]).reduce((actions,action)=>
      Object.assign(actions,{[action]:!userPerms[table][action]})
    ,{})})
  ,{})
}

/**
 * "private" function used by the functions that combine results
 * "private" in the sense that it's not a function that is used outside of this file
 * @param tableList1 the output from getGroupPerms
 * @param tableList2 the output from getGroupPerms
 * @param compareFunc
 * @returns {*}
 */
function combinePermissionSets(tableList1,tableList2,compareFunc) {
  const allPerms=Object.assign({},tableList1,tableList2)
  return Object.keys(allPerms).reduce((tables,table)=>
      Object.assign(tables,{[table]:Object.keys(allPerms[table]).reduce((actions,action)=>
          Object.assign(actions,{[action]:compareFunc(table,action)})
        ,{})})
    ,{})
}

/**
 * Combine two sets of permissions generated from whitelists
 * Permissions granted from either trump permissions revoked in the other
 * If one whitelist has tables the other doesn't, its permissions are obeyed for those tables
 * @param w1 the output from getGroupPerms for the first whitelist
 * @param w2 the output from getGroupPerms for the second whitelist
 */
function combineWhiteResults(w1,w2) {
  function obeyIfExistWithGreedyGrant(table,action) {
    return Boolean((w1[table] && w1[table][action]) || (w2[table] && w2[table][action]))
  }
  return combinePermissionSets(w1,w2,obeyIfExistWithGreedyGrant)
}

/**
 * Combine two sets of permissions generated from a whitelist and blacklist
 * Permissions revoked from either trump permissions granted in the other
 * if blacklist has tables whitelist doesn't, permissions on those tables are revoked
 * if whitelist has tables blacklist doesn't, permissions on those tables obey whitelist permissions
 * @param white the output from getGroupPerms for the whitelist
 * @param black the output from getGroupPerms for the blacklist
 * @returns {*}
 */
function combineWhiteAndBlackResults(white,black) {
  function obeyIfWhiteExistWithGreedyRevoke(table,action) {
    return (!white[table] || (black[table] && !black[table][action])) ? false : (white[table] && white[table][action])
  }
  return combinePermissionSets(white,black,obeyIfWhiteExistWithGreedyRevoke)
}

/**
 * Combine two sets of permissions generated from blacklists
 * Permissions revoked from either trump permissions granted in the other
 * If one blacklist has tables the other doesn't, its permissions are obeyed for those tables
 * @param b1 the output from getGroupPerms for the first blacklist
 * @param b2 the output from getGroupPerms for the second blacklist
 * @returns {*}
 */
function combineBlackResults(b1,b2) {
  const allPerms=Object.assign({},b1,b2)

  function obeyIfExistWithGreedyRevoke(table,action) {
    return ((b1[table] && !b1[table][action]) ||  (b2[table] && !b2[table][action])) ? false : (b1[table] && b1[table][action]) ||  (b2[table] && b2[table][action])
  }
  return Object.keys(allPerms).reduce((tables,table)=>
      Object.assign(tables,{[table]:Object.keys(allPerms[table]).reduce((actions,action)=>
          Object.assign(actions,{[action]:obeyIfExistWithGreedyRevoke(table,action)})
        ,{})})
    ,{})
}

module.exports={
  getGroupPerms,
  hasPerm,
  invertResults,
  combineWhiteResults,
  combineWhiteAndBlackResults,
  combineBlackResults
}