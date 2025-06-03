import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt

def train_nn(X_train, y_train, X_test, y_test):
    class CarPriceNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(10, 64)
            self.fc2 = nn.Linear(64, 32)
            self.out = nn.Linear(32, 1)

        def forward(self, x):
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            return self.out(x)

    model = CarPriceNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.MSELoss()

    losses = []
    for epoch in range(100):
        model.train()
        y_pred = model(X_train)
        loss = loss_fn(y_pred, y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())

    plt.plot(losses)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Loss per Epoch')
    plt.savefig('visuals/nn_loss_plot.png')
    return model