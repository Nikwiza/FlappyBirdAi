 # Actions and states
    states = env.observation_space.shape
    actions = env.action_space.n

    model = build_model(states, actions)
    model.summary()
    print(actions, states)

    dqn = build_agent(model, actions)
    dqn.compile(Adam(lr = 1e-1), metrics = ['mae'])
    dqn.fit(env, nb_steps = 500000, visualize = False, verbose = 1)