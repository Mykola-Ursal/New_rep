# New_rep
ID	Title	Expected result				Status	Comment																		
Registration / Authorization																									
Google account																									
1	User is able to register via Google account	"1. User is registered
2. ""Home"" page is opened"				Passed	Google account																		
2	User is able to authorize via Google account	User is successfully authorized via Google account				Passed																			
3	User is able to register in the system (user needs to authorize in Google account)	"1. The user is redirected to the Google authorization flow
2. Registration is completed only after successful Google authorization."				Passed																			
3	Authorization on the "Sign Up" screen via Google account	"1. User is authoirzed
2. ""Home"" page is opened"				Passed																			
4	Сontinue registration after rejecting Google permissions in the Google consent dialog	After rejecting permissions in the Google consent dialog, the user can restart the Google authorization flow and successfully continue registration.				Passed																			
5	Retry registration after previous Google authorization rejection	The user is able to start Google authorization again and successfully continue the registration flow after a previous rejection.				Passed																			
6	Retry authorization after previous Google authorization rejection	The user is able to restart Google authorization and successfully complete login after a previous rejection				Passed																			
7	User is unauthorized after logout	"1. The user becomes unauthorized after logout. 
2. ""Authorization"" page is opened"				Passed																			
8	User can sign in again after logout	The user can successfully authenticate again after logout using valid credentials.				Passed																			
Login / Password																									
9	Sign up using valid email and password	"1. User successfully completes registration using a valid email and password 
2. User is logged into the system"																							
10	Sign in using valid email and password	"1. User is successfully authorized using a valid email and password 
2. User is redirected to the ""Home"" page"					Login + Password																		
12	Sign up with invalid email format	"1. Registration is not completed
2. A validation error is shown for the email field"																							
	Sign up with email already registered via Google account	"1. Registration using email and password is rejected
2. A validation message is displayed indicating that the email is already associated with a Google account"																							
15	Sign up via Google using an email previously registered with email and password	Registration via Google is completed successfully for an email that already exists in the system as an email/password account (account linking or reuse is handled correctly)																							
15	Sign up using an email that already exists in the system	"1. Registration is rejected
2. A clear validation error message is displayed indicating that the email address is already in use"																							
25	Sign up using a password that does not meet at least one requirement	"1. Registration is not allowed to continue
2. A validation error message is displayed indicating which password requirements are not met"				Passed																			
25	Password length is greater than 8 characters and all other requirements are met	"1. Registration can be continued
2. The password is accepted and no validation error is displayed"				Passed																			
25	Password length is exactly 8 characters and all other requirements are met	"1. Registration can be continued
2. The password is accepted and no validation error is displayed"				Passed																			
26	Password contains Cyrillic characters	"1. Registration is not allowed to continue
2. A validation error message is displayed indicating that unsupported characters are used in the password"				Passed																			
30	Password is equal to the maximum allowed length (256 characters)	"1. Registration can be continued 
2. A validation error message is not displayed"				Passed																			
30	Password exceeds maximum allowed length (257 characters)	"1. Registration cannot be continued 
2. A validation error message is displayed indicating that the maximum password length is exceeded"				Passed																			
32	Return to Sign In form from Sign Up form	"1. Sign In form is opened
2. All registration data is reset"				Passed																			
22	Sign in with invalid email and valid password	"1. Authorization is rejected
2. A validation error message is displayed"				Passed																			
23	Sign in with valid email and invalid password	"1. Authorization is rejected
2. A validation error message is displayed"				Passed																			
24	Sign in with invalid email and invalid password	"1. Authorization is rejected
2. A validation error message is displayed"				Passed																			
33	Continue login after rejecting Google permissions	After rejecting permissions in the Google consent dialog, the user can restart the Google authorization flow and successfully complete authorization				Passed	Fixed: When Afridax project is removed from the “Connected apps and services” section of the Google account used during registration																		
	Sign up using different valid email formats	Registration is successfully completed for all supported valid email formats				Passed																			
34	Display of the validation message when internet connection is lost	"1. Registration is not completed
2. A clear error message about network or connection issues is displayed"				Not tested																			
36	Email with "+1" in domain part is not accepted	"1. Registration is rejected
2. A validation error message is displayed indicating an invalid email address"				Passed																			
Confirm Email Address																									
9	Confirmation email is received during registration	Confirmation email is received when registering with email and password				Not tested																			
	Confirmation email contains the expected text	"1. Email contains the correct confirmation instructions
2. The correct link is shown"				Not tested																			
	Sign in is not allowed after email address is confirmed	"1. If the email address is not confirmed, authorization is rejected
2. Validation message that email confirmation is required is shown
3. Confirmation email is resent"				Not tested																			
	"Authorization" page is opened after clicking the confirmation link	After clicking the confirmation link in the email, the user is redirected to the "Authorization" page				Not tested																			
	Continue authorization using the resent Confirmation email	Authorizaiton is successfully completed using the resent Confirmation email				Not tested																			
	Email address can be confirmed only once	"1. After the email address has already been confirmed, opening the confirmation link again does not change the account state
2. A clear validation message that the email address has already been confirmed is displayed"				Not tested																			
	Email confirmation is not required for Google registration	"1. When the user registers via a Google account, no email confirmation is required 
2. User can authorize without performing email confirmation"				Not tested																			
	Subsequent sign in does not require email confirmation again	After the email address has been successfully confirmed, subsequent authorization attempts are completed successfully without requiring email confirmation again				Not tested																			
2FA																									
38	Sign up via Google Account with 2FA Enabled	"1. Registration is completed successfully
2. The user is required to pass the 2FA verification step and is logged in after successful verification"				Passed																			
39	Sign in via Google account with 2FA enabled	"1. The user is redirected to the 2FA verification step
2. Authorization is completed only after successful 2FA verification"				Passed																			
40	Enable 2FA during Google account registration	2FA setup flow is displayed and must be completed to finish registration				Passed																			
41	Open registration form when 2FA is enabled for Google account	Registration flow is started correctly and includes the mandatory 2FA setup step				Passed																			
42	2FA setup window opens each time until the 2FA setup is completed	2FA setup window is opened each time until the 2FA setup is completed				Passed																			
43	Sign in using email and password with 2FA Enabled	"1. User is redirected to the 2FA verification step after entering valid email and password
2. After entering a valid 2FA code, the user is successfully authorized and redirected to the ""Home"" page"				Passed																			
44	Complete registration with 2FA after an interrupted 2FA setup	If the 2FA setup flow was previously closed or interrupted, the user can reopen the 2FA setup step and successfully complete the 2FA configuration				Passed																			
45	Enable 2FA by scanning a QR code	"1. The QR code is successfully scanned by an authenticator application
2. A valid one-time password generated by the authenticator is accepted and 2FA is enabled for the user account"				Passed																			
48	Enable 2FA by manually entering the setup key	"1. The setup key is accepted by the authenticator application
2. A valid one-time password generated by the authenticator is accepted and 2FA is enabled for the user account"				Passed																			
49	Atempt to complete sign-in using an expired 2FA code	"1. Authorization is rejected
2. A validation error message is displayed indicating that the 2FA code has expired"				Passed																			
49	QR code is still displayed after page reload	"1. Authorization is rejected
2. QR code screen is displayed each time until 2FA is set up"				Passed																			
49	Submit a valid OTP code generated for another account	"1. Authorization is rejected
2. A validation error message is displayed indicating that the 2FA code is invalid"				Passed																			
49	Submit empty OTP code	Authorization cannot be completed				Passed																			
																									
																									
																									
																									
Forgot password																									
52	Open the “Forgot password” page	After clicking the “Forgot Password?” link on the authorization page, the "Forgot password" page is opened				Passed																			
53	Send reset password email to a registered email address	After entering a valid and registered email address and clicking the “Send Reset Link” button, a password reset email is sent to the specified email address.				Passed																			
53	Success toast message is displayed after sending reset link	After a successful request to send the reset password email, a toast notification is displayed indicating that the reset link has been sent.				Passed																			
	Confirmation email contains the expected text	"1. Email contains the correct reset password instructions
2. The correct link is shown"				Not tested																			
	Check that the password reset link can be sent one more time to the same email address	The password reset email can be successfully sent again to the same email address				Not tested																			
	Check that the time limit is set when the user try to send email address in a short delay	"1. If the user attempts to request a reset email multiple times within a short period
2. Request is rejected and a message is displayed indicating that the user must wait before trying again"				Failed																			
	Validation error is shown for invalid email format	After clicking the “Send Reset Link” button with an invalid email address, the request is rejected and a validation error message is displayed				Not tested																			
	Success message is shown for a non-registered email address	"1. After submitting a non-registered email address, a generic success message is displayed (the same as for a registered email)
2. The message does not indicate whether the email address exists in the system and informs the user to check their email if the account exists"				Not tested																			
	Validation error is shown when the email field is empty	After clicking the “Send Reset Link” button with an empty email field, the request is rejected and a validation error message is displayed indicating that the email address is required				Not tested																			
																									
																									
Registration (WhiteList)																									
1	Account creation with whitelisted email (Email flow)	User successfully completes registration and account is created				Passed																			
2	Account creation with whitelisted email (Google OAuth)	User authenticated via Google successfully completes registration if Google email exactly matches whitelist entry				Passed		User can authorize via whitelisted email																	
3	Registration attempt with non-whitelisted email (Email flow)	Registration is terminated immediately and user receives exact error message: "Account cannot be created at this time. Please contact support". No account is created				Passed		User cannot authorize via whitelisted email																	
4	Registration attempt with non-whitelisted email (Google OAuth)	Registration is terminated immediately and user receives exact error message: "Account cannot be created at this time. Please contact support". No account is created				Passed		All existing funcitonality related to the chainging credentials work as expected for whitelisted email																	
5	Exact match validation against whitelist	Access is granted only when email exactly matches whitelist entry				Passed		All existing funcitonality related to the chainging credentials work as expected for non-whitelisted email																	
6	Case-insensitive email comparison during whitelist validation	Registration succeeds regardless of email letter case if business rule defines case-insensitive comparison				Skipped		2FA works																	
7	No user entity creation after failed whitelist validation	No user profile, wallet, session, or related resources are created in database when whitelist validation fails				Passed																			
8	Registration blocking does not affect an existing user					Passed																			
9	Whitelist validation executed before account creation logic	System performs whitelist check prior to creating any user-related records				Not tested																			
10	Registration blocked after email removal from whitelist	New registration attempts are rejected once email is removed from whitelist				Passed																			
11	Registration blocked after setting false for an email	New registration attempts are rejected once email is removed from whitelist				Passed																			
12	Exact error message for unauthorized registration	System returns exactly: "Account cannot be created at this time. Please contact support" without deviations				Passed																			
13	Consistent HTTP status code for whitelist rejection	Backend returns defined and consistent HTTP status code (e.g.				Not tested																			
14	No confirmation email sent for non-whitelisted registration attempt	System does not trigger confirmation email when whitelist validation fails				Passed																			
15	Confirmation screen displayed after successful registration	Confirmation screen is shown only after successful account creation				Passed																			
16	Password reset for successfully registered user	Password reset flow works for existing registered account				Passed																			
17	Password reset request for non-existing email					Passed																			
18	2FA setup available after successful registration	2FA setup flow works only after successful whitelist validation and account creation				Passed																			
19	2FA enforcement during login	User with enabled 2FA must complete verification to access account				Passed																			
20	Direct API registration attempt with non-whitelisted email	API request is rejected with same exact error message and no user record is created				Not tested																			
21	Duplicate email insertion into whitelist	Database prevents duplicate email entries if unique constraint is configured				Not tested																			
22	Whitelist changes applied without system restart	Adding or removing email from whitelist takes effect immediately without requiring service restart				Passed																			
23	Registration stops in the middle (email is not confirmed)					Passed																			
24	Concurrent registration requests					Passed																			
25	Registration of an email address that already is registered 	Validation error is displayed				Passed																			
26	Changing credentials in the "Settings" works as expected					Passed																			
Additonal checkings (WhiteList)																									
1	Invite is sent to the correct email address					Passed																			
	Redirection to the "Registration" page via the link in the email	"Sign Up" page is opened				Passed																			
	User is able to register in an invitation flow					Passed																			
	Check that a new registered user can invite another user					Passed																			
	Check that a new registered user can invite another user before a first wallet is created					Passed																			
	Validation error display if invitation has been already sent to this email					Passed																			
	Validation error display if email address has been already registered					Passed																			
	Validation display if an invalid email is entered					Passed	Validation error message is not shown, but the action buttion is disabled																		
	Spam check (only 10 invitation can be sent)					Passed																			
	Check if user is not register for some minutes after the email is confirmed					Passed																			
	Generic error fallback: "Something went wrong. Please try again later."					Passed																			
	Loader					Passed																			
	Success toat message					Passed																			
	Try to register when user is not confirmed invitation yet					Passed																			
	Authorization via Google account that is added to whitelist					Passed																			
	User firstly tries to register as non-whitelisted and when after getting an invitation as whitelisted					Passed																			
	Reset password flow is not broken					Passed																			
	Confirm email is not broken					Passed																			
	When non-whitelisted email address that has been successfully changed in Settings uses for authorization					Passed																			
User Interface / User Experience																									
	Unauthorized user is redirected to Sign Up page when opening invitation link	When an unauthorized user opens the invitation link from the email, the user is redirected to the Sign Up page				Passed																			
	Authorized user is redirected to Dashboard when opening invitation link	When an authorized user opens the invitation link from the email, the system redirects the user directly to the Dashboard				Passed																			
	Invitation link without signup route redirects user to Log In page	If the invitation link does not contain a signup route parameter, the user is redirected to the Log In page				Passed																			
	Page remains on Sign Up after reload when invitation link contains signup route	After reloading the page opened from an invitation link containing the signup route, the Sign Up page remains displayed				Passed																			
	Page remains on Log In after reload when invitation link does not contain signup route	After reloading the page opened from an invitation link without the signup route, the Log In page remains displayed.				Passed																			
	Invitation link opens Sign Up tab by default	When opening the invitation link, the Sign Up tab is selected by default and the Log In tab is not active.				Passed																			
	Manual switch from Sign Up to Log In does not break invitation flow	User can manually switch to the Log In tab and the page loads correctly without breaking the invitation flow.				Passed																			
	Direct navigation to invitation link opens Sign Up page	When the invitation link is pasted directly into the browser address bar, the Sign Up page is displayed.				Passed																			
	Invitation link works correctly in a new browser session	When opening the invitation link in a new browser session without authorization, the Sign Up page is displayed.				Passed																			
2FA (iframe)																									
	2FA iframe is displayed after successful email and password login when 2FA is enabled	User enters valid email and password  Application redirects to the 2FA verification page  OTP input is rendered inside a secure isolated iframe				Passed																			
	Successful authentication using valid OTP inside iframe	User enters valid OTP inside the iframe  Backend confirms OTP validity  Iframe sends a secure success message via postMessage  Parent window initializes the user session				Passed																			
	Authentication is blocked when OTP entered in iframe is invalid	User enters invalid OTP inside the iframe  Backend rejects the OTP  Error message is displayed  User session is not initialized				Passed																			
	2FA setup during registration renders QR code inside secure iframe	User enables 2FA during registration  Registration modal opens  QR code and secret are generated  QR code and secret are rendered only inside the iframe				Passed																			
	2FA setup from account settings renders QR code inside secure iframe	User opens account settings  User selects Enable 2FA  Application loads iframe  QR code and secret are displayed inside the iframe				Passed																			
	Session context is passed securely from parent window to iframe during 2FA setup	User enables 2FA from settings  Parent window sends session context to iframe  Iframe successfully renders QR code using the session context				Passed																			
	Secure postMessage communication is used after successful OTP validation	User enters valid OTP  Iframe validates OTP with backend  Iframe sends secure success message using postMessage  Parent window receives message and initializes session				Passed																			
	User cannot access QR code or 2FA secret via main application context	QR code and secret are rendered inside iframe  Attempting to access QR or secret from browser console returns no data  Sensitive information is not exposed in parent application state				Passed																			
	2FA requirement is enforced for newly registered users without enabled 2FA (email registration)	User registers using email and password without enabling 2FA  Application requires enabling 2FA before full access is granted				Passed																			
	2FA requirement is not enforced when 2FA was enabled during email registration	User registers using email and password and enables 2FA during registration  Account access is granted without additional 2FA requirement modal				Passed																			
	2FA requirement is enforced for newly registered users without enabled 2FA (Google registration)	User registers using Google account without enabling 2FA  Application requires enabling 2FA before full access is granted				Passed																			
	2FA requirement is not enforced when 2FA was enabled during Google registration	User registers using Google account and enables 2FA during registration  Account access is granted without additional 2FA requirement modal				Passed																			
	User cannot create the first wallet until 2FA is enabled	User attempts to create the first wallet  System checks 2FA status  Wallet creation is blocked if 2FA is not enabled				Passed																			
	Navigation between application pages is restricted until 2FA is enabled	User attempts to navigate to another page without enabling 2FA  Navigation is blocked  2FA setup modal remains active				Passed																			
	User session is terminated when the 2FA setup modal is closed	User closes the 2FA setup modal without completing the process  User session is invalidated  User is logged out				Passed																			
	User session is terminated after page reload when 2FA setup was not completed	User reloads the page during mandatory 2FA setup  Session validation occurs  User is logged out and must authenticate again				Passed																			
	2FA setup modal appears again if user attempts login without completing required 2FA setup	User previously skipped mandatory 2FA setup  User logs in again  Application shows the 2FA setup modal				Passed																			
	Successful confirmation message is shown after enabling 2FA	User completes OTP verification during 2FA setup  2FA is successfully enabled  Success confirmation message is displayed				Failed																			
	Disabling 2FA requires valid OTP confirmation	User attempts to disable 2FA in settings  User enters OTP  2FA is disabled only if OTP is valid				Passed																			
	Disabling 2FA fails when OTP confirmation is invalid	User attempts to disable 2FA  User enters invalid OTP  System rejects the request  2FA remains enabled				Passed																			
						Passed																			
User Interface / User Experience																									
	2FA iframe is visually isolated from the parent application interface	2FA verification screen is displayed  OTP form is rendered inside iframe  Iframe visually appears as a separate secure component				Passed																			
	2FA modal is centered and properly displayed during registration flow	User selects enable 2FA during registration  Modal appears centered  Iframe content loads correctly				Passed																			
	OTP input fields are clearly visible and accessible inside iframe	OTP verification screen loads  Input fields are visible  User can enter digits without UI issues				Passed																			
	QR code is clearly visible inside the iframe during 2FA setup	User opens 2FA setup  QR code is rendered inside iframe  QR code is readable and scannable				Passed																			
	Error message is displayed when OTP validation fails	User enters invalid OTP  Validation occurs  Error message is clearly visible to the user				Passed																			
	Success message is displayed after successful 2FA activation	User completes OTP verification  System confirms activation  Success message appears				Failed																			
	2FA setup modal cannot be bypassed when it is mandatory	User attempts to interact with background UI  Background interaction is disabled  2FA modal remains active				Not tested																			
	2FA iframe loads without layout shifting or visual glitches	User navigates to 2FA screen  Iframe loads  Layout remains stable without UI shifts				Failed																			
	OTP input allows numeric entry only	User attempts to enter characters  Non-numeric input is rejected  Only digits are accepted				Passed																			
	Loading state is displayed while iframe initializes	2FA screen loads  Iframe initialization occurs  Loading indicator is displayed until iframe content appears				Passed																			
																									
2FA restriction																									
	User is required to enable 2FA when force2FA = true	User cannot continue working with regular wallets, Vaults, Address Book until Two-Factor Authentication is configured				Passed																			
	2FA requirement is removed after switching force2FA from true to false	User can access the Vault, regular wallet, Address Book without being prompted to enable 2FA after force2FA is changed from true to false				Passed																			
	User authorization is completed without 2FA when force2FA is disabled	User successfully logs in and accesses the Vault, regular wallet, Address book without a 2FA prompt after force2FA is switched to false				Passed																			
	User cannot access Vault interface while 2FA setup is required	All Vault functionality remains inaccessible until 2FA setup is completed				Passed																			
	2FA setup modal reappears after disabling 2FA when force2FA = true	After disabling 2FA the system immediately prompts the user to configure 2FA again and blocks further interaction				Passed																			
	2FA remains enabled after email change	User email is successfully updated and Two-Factor Authentication remains active				Passed																			
	2FA can be disabled after email change	User successfully disables Two-Factor Authentication after updating email				Passed																			
	2FA can be enabled after email change	User successfully enables Two-Factor Authentication after updating email				Passed																			
	2FA remains enabled after password change	User password is successfully updated and Two-Factor Authentication remains active				Passed																			
	2FA can be disabled after password change	User successfully disables Two-Factor Authentication after updating password				Passed																			
	2FA can be enabled after password change	User successfully enables Two-Factor Authentication after updating password				Passed																			
	Email change is saved successfully	User email is updated and displayed as the current email in profile settings				Passed																			
	Password change is saved successfully	User password is updated and user can authenticate with the new password				Passed																			
	Authenticator code is required to disable 2FA	2FA is disabled only after entering a valid 6-digit authenticator code				Passed																			
	Invalid authenticator code prevents disabling 2FA	System displays an error and 2FA remains enabled				Passed																			
	Google account connection status persists after email change	Google account remains connected after updating email				Passed																			
	Google account connection status persists after password change	Google account remains connected after updating password				Passed																			
	Attention modal is displayed	"1. The ""Attention"" modal is displayed immediately after an action related to the Vault, regular wallet, or Address Book is performed 
2. The ""Attention"" modal is displayed each time before the main 2FA modal appears"				Passed																			
	Attention modal closing	The "Attention" modal closes after clicking the action button, the close button, or outside the modal				Passed																			
User Interface / User Experience																									
	Disable 2FA button is visible when Two-Factor Authentication is enabled	The Disable 2FA button is displayed in the Security section				Passed																			
	Disable 2FA button opens confirmation flow	User is prompted to enter a 6-digit authenticator code before 2FA is disabled				Passed																			
	2FA information text is displayed in the Security section	Instructional text explaining authenticator usage is visible to the user				Passed																			
	Attention modal contains clear and understandable text	The "Attention" modal displays clear and understandable text explaining the purpose of the action and informing the user about the upcoming 2FA confirmation				Passed																			
																									
Restrict export / import functionality																									
1	For existing user export	"1. Import doest not allow on the ""Wallet"" page for an existing user
2. Import doest not allow on the ""Settings"" page for an existing user"				Passed																			
	For a new user export 	"1. Import doest not allow on the ""Wallet"" page for a new user
2. Import doest not allow on the ""Settings"" page for a new user"				Passed																			
	For existing user import	"1. Import doest not allow on the ""Wallet"" page for an existing user
2. Import doest not allow on the ""Settings"" page for an existing user"				Passed																			
	For a new user import 	"1. Import doest not allow on the ""Wallet"" page for a new user
2. Import doest not allow on the ""Settings"" page for a new user"				Passed																			
	Check that other functionality works as expected					Passed																			
	Export / import cannot be compelted if variable in env. switch to TRUE					Passed																			
Adress Book forсe mode								Solana	Tron	BTC	XRP 	Cardano													
1	Sending from a regular wallet					Passed		Passed	Passed	Passed	Passed	Passed													
	Sending from a Vault					Passed		Passed	Passed	Not tested	Passed	Passed													
	Validation error message for adresses that does not exist in the Address book (regular wallet)					Passed		Passed	Passed	Passed	Passed	Passed													
	Validation error message for adresses that does not exist in the Address book (Vault)					Passed	Solana: When Proposal transaction is created with non-whitelisted email address, an unclear validation error message is shown	Failed	Passed	Not tested	Passed	Passed													
	Sending Contact with memo					Skipped		Passed	Passed	Skipped	Passed	Skipped													
	Adrdress book contact saved in one account does not affect on withdrawal from another account					Passed		Passed	Passed	Passed	Passed	Passed													
	Address book Force mode does not work after switching it to false in .env					Passed																			
Email recover								ROLE																	
	Email address is successfully updated after confirmation	User email in account settings and database is updated to the new email address				Passed		User can recover email address, and can used a new one																	
	Old email address cannot be used for authorization after the change is completed	Authorization with the old email fails and system displays an invalid credentials error				Passed																			
	New email address can be used for authorization after the change	User successfully logs in using the new email address and password				Passed																			
	Recovery email is sent to the old email address after email change request	Old email receives an email containing a recovery link to revert the email change				Passed																			
	Email change can be reverted using the recovery link	User email is restored to the previous email address after the recovery link is used				Passed																			
	Recovery link cannot be reused after successful recovery	System displays an error indicating the link is invalid or already used				Passed																			
	Email recovery cycle can be completed twice	User can perform email change and recovery twice without system errors				Passed																			
	Email recovery cycle can be repeated with the same email addresses	System allows repeating the email change and recovery process using the same pair of email addresses				Passed																			
	Email change request does not affect active user session	User remains logged in after initiating email change				Passed																			
	Active session authorized with the old email when a new email is confirmed	The active session is automatically terminated after the new email address is confirmed and the user is required to log in again using the new email				Passed																			
	Active session authorized with the new email when email reset is completed	The active session is automatically terminated after the email reset is completed and the user is required to log in again using the restored email address				Passed																			
	Email change request fails if the new email is already used by another account	System displays an error indicating the email address is already taken				Passed																			
	Email change request fails if the new email format is invalid	System displays a validation error for invalid email format				Passed																			
	Recovery link works only for the corresponding account	Recovery link restores email only for the user account that initiated the change				Passed																			
	Expired recovery link cannot be used	System displays an error indicating the recovery link has expired				Passed																			
	Multiple email change requests generate separate recovery emails	Each request sends a new recovery email and invalidates previous recovery links				Passed																			
User Interface / User Experience																									
	Confirmation message appears after submitting email change request	System informs the user that a confirmation or notification email has been sent				Passed																			
	Recovery email contains a clear explanation of the action	Email explains that the user can revert the email change using the provided link				Passed																			
	Recovery email contains a visible and clickable recovery link	User can easily locate and click the recovery link in the email				Passed																			
	Error message is displayed when recovery link is invalid or already used	User sees a clear message explaining why the recovery action failed				Passed																			
	Success message is displayed after successful email recovery	User sees confirmation that the email address has been restored				Passed																			
																									
																									
Responsive / Mobile																									
ID	UI Checks	Android	iPhone	Tablet	Comment																				
	General layout																								
	Verify that the layout is not broken on mobile screens																								
	Verify that no horizontal scrolling is present																								
	Verify that all UI elements fit within the screen width																								
	Verify that content is not cut off or overlapped																								
	Text & readability																								
	Verify that text is readable without zooming																								
	Verify that font sizes and line spacing are consistent																								
	Verify that labels and placeholders are fully visible																								
	Buttons & interactive elements																								
	Verify that all buttons are visible and tappable																								
	Verify that buttons are not overlapped by other elements																								
	Verify that touch targets meet minimum size requirements																								
	Modals & popups																								
	Verify that modals fit the mobile screen																								
	Verify that modal content is scrollable when needed																								
	Verify that modal close actions are accessible																								
	Keyboard & input fields																								
	Verify that the on-screen keyboard does not overlap input fields																								
	Verify that the focused input field is visible when the keyboard is open																								
	Verify that the screen scrolls correctly to the active input																								
	Verify that input fields are usable in both portrait and landscape modes																								
	Orientation & navigation																								
	Verify that UI adapts correctly when switching orientation																								
	Verify that navigation elements remain accessible after rotation																								
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
																									
