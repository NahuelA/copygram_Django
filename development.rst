create post model
create profile model
  GLOSARY
- F: "Fix"
- T: "Tested"
- NT: "Not tested"
- C: "Complete"
- I: "Incomplete"
- A: "Add"
- //: "Verbose information"

######################
#  Development goals
######################

## Backend apps:

********************
### Direct message
********************
  - *C* | List DM
  - *C* | Send DM
  - *I* | Delete DM
  - *I* | Blocked profile
---
  - Validations:
    - *I* | Send message for their contacts
    - *I* | If the profile is blocked, not receive or send message.
    - *C* | If profile doesn't exists, not send message
---
  - Serializers:
    - *C* | DM:

***********
### Posts
***********
  - *I*    | Pagination
  - *C*    | List posts
  - *C*    | Create Posts
  - *I-T*  | Edit Posts
  - *C*    | Like posts
  - *C*    | Comments posts
  - *I*    | Share posts
  - *C*    | Search profile
  - *C-NT* | Save posts
---
  - Validations:
    - *I*    | List posts from profiles that are user follow.
    - *I*    | Profile will be able to edit their posts.
    - *C*    | Rate only once
---
  - Serializers:
    - *C-NT* | Califications
    - *C* | Comments
    - *C-NT* | Post saves
    - *C* | Posts

*************
### Profile
*************
  - *I*    | Pagination
  - *C*    | List profile
  - *C*    | Create Profile
  - *C*    | Edit profile
  - *C-NT* | Delete profile
  - *C*    | Followers
  - *C*    | Following
---
  - Validations:
    - *I* | Make a validation when change profile picture, if
            a new image is detected, delete the old picture.
    - *C* | Update their posts and profile, validate token.
---
  - Serializers:
    - *C*    | Profile
    - *C*    | Followers
    - *C*    | Following
    - *C*    | Users
    - *C*    | VerifyUser
    - *C*    | VerifyToken

************
#### Login
************
  - *C*   | Logout
  - *I*   | Forgot your password?
  - *I*   | Password_change
  - *I*   | Password_change_done
  - *I*   | Password_reset
  - *I*   | Password_reset_done
  - *I*   | Password_reset_confirm
  - *I*   | Password_reset_complete
---
  - Validations:
    - *C* | If invalid credentials, invalid login.
    - *C* | If not active, ask to verify your account.
    - *I* | Validation change password.
---
  - Serializers:
    - *C* | Login

**************
#### Sign-up
**************
  - *C* | Sign-up user
---
  - Validations:
    - *C* | Only one user with that username and email.
    - *C* | Password with a minimum length to 8 chars.
    - *C* | Verify account throught a token with jwt.
