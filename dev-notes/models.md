# SimpleContact
- name
- gender
- phones[]
- email


# ProjectMember(SimpleContact)
- username
- type (internal, guest)
- role (visitor, client, expert)

# User(SimpleContact)
- username
- isLicenseContact
- isVerified
- isDisabled
- userRoles[] (project-creator, project-admin)


## Client
- name
- description
- address
- phones[]
- fax
- website
- contacts[] (SimpleContact)

## Contract
- clientId
- signee (client, SimpleContact)
- signedBy (company, name)
- startDate
- endDate
- type (typed, uniform)
- pricing[]*
  - module
  - level1
  - level2
  - level3
 - terms
 - status

 * untuk tipe dg pricing seragam, level 1, 2, 3 diisi sama

## Project
- licenseId
- contractId
- name
- description
- lead (name)
- clientLead (name)
- startDate
- endDate
- status
- guests (person, ProjectGuest)


ContractInfo
- client
- contract


## Note (can be applied to any model)
- note
- noteOn (target ObjectId)
- noteBy
- createdAt
