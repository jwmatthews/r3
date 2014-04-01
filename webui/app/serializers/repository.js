/*

Example from Pulp 2.4
GET /pulp/api/v2/repositories/


[
    {
        "_href": "/pulp/api/v2/repositories/pulp_unittest/",
        "_id": {
            "$oid": "5335a657f0891d0b1e323ca0"
        },
        "_ns": "repos",
        "content_unit_counts": {
            "distribution": 1,
            "erratum": 52,
            "package_category": 2,
            "package_group": 3,
            "rpm": 3
        },
        "description": null,
        "display_name": "pulp_unittest",
        "id": "pulp_unittest",
        "notes": {
            "_repo-type": "rpm-repo"
        }
    }
]

Ember Data wants the data to be in the format of
[
  "repository": 
  [
    {
        "_href": "/pulp/api/v2/repositories/pulp_unittest/",
        "_id": {
            "$oid": "5335a657f0891d0b1e323ca0"
        },
        "_ns": "repos",
        "content_unit_counts": {
            "distribution": 1,
            "erratum": 52,
            "package_category": 2,
            "package_group": 3,
            "rpm": 3
        },
        "description": null,
        "display_name": "pulp_unittest",
        "id": "pulp_unittest",
        "notes": {
            "_repo-type": "rpm-repo"
        }
    }
  ]
]



Example from Pulp 2.4
GET /pulp/api/v2/repositories/pulp_unitest/

{
    "_href": "/pulp/api/v2/repositories/pulp_unittest/",
    "_id": {
        "$oid": "5335a657f0891d0b1e323ca0"
    },
    "_ns": "repos",
    "content_unit_counts": {
        "distribution": 1,
        "erratum": 52,
        "package_category": 2,
        "package_group": 3,
        "rpm": 3
    },
    "description": null,
    "display_name": "pulp_unittest",
    "id": "pulp_unittest",
    "notes": {
        "_repo-type": "rpm-repo"
    },
    "scratchpad": {
        "checksum_type": "sha256"
    }
}
*/
var RepositorySerializer = DS.RESTSerializer.extend({
  normalizePayload: function(primaryType, payload) {
    console.log("<RepositorySerializer> normalizePayload("+primaryType+", "+payload+")");
    var mod_payload = {};
    mod_payload["repository"] = payload;
    return this._super(primaryType, mod_payload);
  }
});

export default RepositorySerializer;