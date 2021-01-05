# Safe Ministry Bot

This bot is designed to be added to a [Discord](https://discord.com/) server, to make the server compliant with the Anglican Diocese of Sydney's Safe Ministry guidelines, and hence suitable for a youth group community.

[//]: # "Why have a Discord server?"
Hosting an official Discord server creates opportunities for youth to deepen their sense of community with both each other and their leaders. Interacting throughout the week provides more space for mutual encouragement, modelling Christian living and even new friendships to develop. A stronger sense of connection to the youth community also has the potential to lead to deeper discussions while on church grounds, positively impacting important ministries such as Bible Study.

Particularly relevant during the COVID-19 era is how Discord creates a positive online space for people to both formally and casually interact when meeting in person is not an option.

***What activities might happen on a youth Discord server?***
- Sharing Bible verses throughout the week; encouraging one another to read the Bible
- ???
- Playing computer games together
- Hosting Bible study or even youth group if meeting in person is not an option

It achieves this by automatically enforcing a set of rules, restricting forms of communication between youth group members and their leaders that would otherwise make a Discord server unsuitable for this interaction.  ~~The bot also has some additional functionality to make the running of such a server more convenient~~

*List of functionality*

This bot (a program that can perform tasks automatically) is designed to be used in conjunction with a suitably configured Discord server to enable young people of youth group age and their leaders to communicate together in a group setting online, while adhering to Safe Ministry guidelines. The primary feature that sets Discord apart from other social media platforms is the fact that it offers voice communication - this also presents additional Safe Ministry challenges, and is one of the problems that this bot has been created to solve.

The following source material was used as the basis for the Safe Ministry guidelines that the Discord server follows / this bot enforces:  
- [Social Contact Policy v3.1](https://safeministry.org.au/wp-content/uploads/pdf/PSU_SocialContactPolicy_v3_1.pdf)
  - Social media sections
- [Safe Ministry Blueprint for Youth Ministry Leaders](https://safeministry.org.au/wp-content/uploads/pdf/SM-BlueprintForYthMinLeaders.pdf)
  - Section 5: The Golden Rules
  - Section 5.g: Communication
- [COVID-19 - Using Video Conferencing](https://safeministry.org.au/covid-19-principles-when-using-video-conferencing/?fbclid=IwAR33oCo0xghOn5uiSCGxzwrUQnvTMpXEG7nUpol0GNGCiKyvuI0MFoDnWoo)
  - A lot of the principles from this page have been applied, though no video functionality is allowed on the Discord server.
  
## Setup

***But wait, how do the Safe Ministry guidelines allow a youth discord server to exist?***  
Most of the guidelines regarding online interaction address one-to-one conversations, such as phone calls, texts and emails. The discord server that this bot is designed to reside in is built to facilitate group interaction between multiple young people and leaders, never one-to-one communication. As such, the server most closely falls into the category of 'Social Media' for the first two documents listed above, rendering it subject primarily to 'The Ten' outlined in the [Safe Ministry Blueprint for Youth Ministry Leaders](https://safeministry.org.au/wp-content/uploads/pdf/SM-BlueprintForYthMinLeaders.pdf), and 'discretion'.

*Link discord server template*

***So what's the bot for?***  
Discord allows for groups of members to interact in text 'channels', much like a youth group Facebook page where all conversations are visible to everyone in the group. Discord also has voice channels however, which allow for what are effectively group phone calls. The Safe Ministry guidelines do not directly address *group* phone calls, so instead we must apply the principles outlined elsewhere in the guideline, namely 'The Golden Rules'.

Without modification, Discord could allow one young person and one leader to join a voice channel together, which would be a breach of the golden rules 'Two or More' and 'Never Alone'. With this bot in the server, it will prevent group members from hearing each other until there are at least two leaders in the voice channel, thus 'enforcing' the Safe Ministry guideline.